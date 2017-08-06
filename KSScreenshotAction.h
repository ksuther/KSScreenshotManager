/*
 * KSScreenshotAction.h
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

#import <Foundation/Foundation.h>

@class KSScreenshotManager;

@interface KSScreenshotAction : NSObject

@property(nonatomic, strong) NSString *name;
@property(nonatomic, assign) BOOL asynchronous;
@property(nonatomic, copy) void(^actionBlock)();
@property(nonatomic, copy) void(^cleanupBlock)();
@property(nonatomic, assign) BOOL includeStatusBar; //defaults to NO, which means the status bar will be cropped out
@property(nonatomic, weak) KSScreenshotManager *manager; //set by addScreenshotAction:, you don't have to set this yourself

+ (instancetype)actionWithName:(NSString *)name asynchronous:(BOOL)asynchronous actionBlock:(void(^)(void))actionBlock cleanupBlock:(void(^)(void))cleanupBlock;

/**
 * Encapsulates a screenshot action. The real portion of interest is the asynchronous flag. If set to NO, the screenshot will be taken immediately after
 * actionBlock is called. If set to YES, then it is up to the action to call -[KSScreenshotManager actionIsReady] to trigger the screenshot and continue
 * to the next action. This is useful for setting up screenshots that require complex UI setup, a network connection, or other things that can't be done
 * easily by just spinning the run loop.
 *
 * @param name The name of the screenshot. This will be included in the screenshot file name.
 * @param asynchronous Indicates whether the action will asynchronously signal when it is ready.
 * @param actionBlock Block to set up the screenshot.
 * @param cleanupBlock Block called after the screenshot is taken. Can be nil.
 */
- (id)initWithName:(NSString *)name asynchronous:(BOOL)asynchronous actionBlock:(void(^)(void))actionBlock cleanupBlock:(void(^)(void))cleanupBlock;

@end

#endif
