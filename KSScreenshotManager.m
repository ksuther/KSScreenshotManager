/*
 * KSScreenshotManager.m
 *
 * Copyright (c) 2013 Kent Sutherland
 * 
 * Permission is hereby granted, free of charge, to any person obtaining a copy of
 * this software and associated documentation files (the "Software"), to deal in
 * the Software without restriction, including without limitation the rights to use,
 * copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the
 * Software, and to permit persons to whom the Software is furnished to do so,
 * subject to the following conditions:
 * 
 * The above copyright notice and this permission notice shall be included in all
 * copies or substantial portions of the Software.
 * 
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
 * FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
 * COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
 * IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
 * CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
 */

#if CREATING_SCREENSHOTS

#import "KSScreenshotManager.h"
#import "KSScreenshotAction.h"

CGImageRef UIGetScreenImage(); //private API for getting an image of the entire screen

@interface KSScreenshotManager ()
@property(nonatomic, strong) NSMutableArray *screenshotActions;
@end

@implementation KSScreenshotManager

- (id)init
{
    if ( (self = [super init]) ) {
        NSArray *arguments = [[NSProcessInfo processInfo] arguments];
        
        //Prefer taking the last launch argument. This allows us to specify an output path when running with WaxSim.
        if ([arguments count] > 1) {
            NSString *savePath = [[arguments lastObject] stringByExpandingTildeInPath];
            
            [self setScreenshotsURL:[NSURL fileURLWithPath:savePath]];
        } else {
            NSString *documentsPath = [NSSearchPathForDirectoriesInDomains(NSDocumentDirectory, NSUserDomainMask, YES) lastObject];
            
            [self setScreenshotsURL:[NSURL fileURLWithPath:documentsPath]];
        }
    }
    return self;
}

- (void)takeScreenshots
{
    [self setupScreenshotActions];
    
    if ([[self screenshotActions] count] == 0) {
        [NSException raise:NSInternalInconsistencyException format:@"No screenshot actions have been defined. Unable to take screenshots."];
    }
    
    [self takeNextScreenshot];
}

- (void)takeNextScreenshot
{
    if ([[self screenshotActions] count] > 0) {
        KSScreenshotAction *nextAction = [[self screenshotActions] objectAtIndex:0];
        
        if ([nextAction actionBlock]) {
            [nextAction actionBlock]();
        }
        
        if (![nextAction asynchronous]) {
            //synchronous actions can run immediately
            //asynchronous actions need to call actionIsReady manually
            [self actionIsReady];
        }
    } else {
        exit(0);
    }
}

- (void)actionIsReady
{
    CFRunLoopRunInMode(kCFRunLoopDefaultMode, 0.1, false); //spin the run loop to give the UI a chance to catch up
    
    KSScreenshotAction *nextAction = [[self screenshotActions] objectAtIndex:0];
    
    [self saveScreenshot:[nextAction name] includeStatusBar:[nextAction includeStatusBar]];
    
    if ([nextAction cleanupBlock]) {
        [nextAction cleanupBlock]();
    }
    
    [[self screenshotActions] removeObjectAtIndex:0];
    
    [self takeNextScreenshot];
}

- (void)setupScreenshotActions
{
    [NSException raise:NSInternalInconsistencyException format:@"You must override %@ in a subclass", NSStringFromSelector(_cmd)];
}

- (void)addScreenshotAction:(KSScreenshotAction *)screenshotAction
{
    if (!_screenshotActions) {
        [self setScreenshotActions:[NSMutableArray array]];
    }
    
    [screenshotAction setManager:self];
    
    [[self screenshotActions] addObject:screenshotAction];
}

- (void)saveScreenshot:(NSString *)name includeStatusBar:(BOOL)includeStatusBar
{
    //Get image with status bar cropped out
    CGFloat StatusBarHeight = [[UIScreen mainScreen] scale] == 1 ? 20 : 40;
    CGImageRef CGImage = UIGetScreenImage();
    BOOL isPortrait = UIInterfaceOrientationIsPortrait([[UIApplication sharedApplication] statusBarOrientation]);
    CGRect imageRect;
    
    if (!includeStatusBar) {
        if (isPortrait) {
            imageRect = CGRectMake(0, StatusBarHeight, CGImageGetWidth(CGImage), CGImageGetHeight(CGImage) - StatusBarHeight);
        } else {
            imageRect = CGRectMake(StatusBarHeight, 0, CGImageGetWidth(CGImage) - StatusBarHeight, CGImageGetHeight(CGImage));
        }
        
        CGImage = (__bridge CGImageRef)CFBridgingRelease(CGImageCreateWithImageInRect(CGImage, imageRect));
    }
    
    NSString *devicePrefix = nil;
    
    if (UI_USER_INTERFACE_IDIOM() == UIUserInterfaceIdiomPhone) {
        devicePrefix = [NSString stringWithFormat:@"iphone%.0f", CGRectGetHeight([[UIScreen mainScreen] bounds])];
    } else {
        devicePrefix = @"ipad";
    }
    
    UIImage *image = [UIImage imageWithCGImage:CGImage];
    NSData *data = UIImagePNGRepresentation(image);
    NSString *file = [NSString stringWithFormat:@"%@-%@-%@.png", devicePrefix, [[NSLocale currentLocale] localeIdentifier], name];
    NSURL *fileURL = [[self screenshotsURL] URLByAppendingPathComponent:file];
    
    NSLog(@"Saving screenshot: %@", [fileURL path]);
    
    [data writeToURL:fileURL atomically:YES];
}

@end

#endif
