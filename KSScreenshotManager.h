/*
 * KSScreenshotManager.h
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

@class KSScreenshotAction;

@interface KSScreenshotManager : NSObject

/**
 * Path to save screenshots
 * Defaults to the last argument in -[NSProcessInfo arguments] so you can specify a save directory from the command line.
 * Falls back to saving in the app's Documents directory if no argument is found
 * Set this before calling takeScreenshots to specify your own place to save screenshots
 */
@property(nonatomic, retain) NSURL *screenshotsURL;

/**
 * Whether or not the simulator closes after all screenshot actions finish
 * Defaults to YES
 */
@property(nonatomic, assign, getter = doesExitOnComplete) BOOL exitOnComplete;

/**
 * Begin taking screenshots. Exits when complete.
 */
- (void)takeScreenshots;

/**
 * Subclass and return an array of KSScreenshotActions
 *
 * You shouldn't need to call this yourself
 */
- (void)setupScreenshotActions;

/**
 * Call in your setupScreenshotActions subclass
 */
- (void)addScreenshotAction:(KSScreenshotAction *)screenshotAction;

/**
 * Called by asynchronous actions to signal that the screenshot manager should take a screenshot and continue to the next action.
 * Synchronous actions will call this automatically.
 */
- (void)actionIsReady;

@end

#endif
