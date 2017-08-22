/*
 * KSScreenshotAction.m
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

#import "KSScreenshotAction.h"
#import "KSScreenshotManager.h"

@implementation KSScreenshotAction

+ (instancetype)actionWithName:(NSString *)name asynchronous:(BOOL)asynchronous actionBlock:(void(^)(void))actionBlock cleanupBlock:(void(^)(void))cleanupBlock
{
    return [[self alloc] initWithName:name asynchronous:asynchronous actionBlock:actionBlock cleanupBlock:cleanupBlock];
}

- (id)initWithName:(NSString *)name asynchronous:(BOOL)asynchronous actionBlock:(void(^)(void))actionBlock cleanupBlock:(void(^)(void))cleanupBlock
{
    if ( (self = [super init]) ) {
        [self setName:name];
        [self setAsynchronous:asynchronous];
        [self setActionBlock:actionBlock];
        [self setCleanupBlock:cleanupBlock];
    }
    return self;
}

@end

#endif
