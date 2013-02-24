//
//  MyScreenshotManager.h
//  KSScreenshotManagerExample
//
//  Created by Kent Sutherland on 2/10/13.
//  Copyright (c) 2013 Kent Sutherland. All rights reserved.
//

#if CREATING_SCREENSHOTS

#import <UIKit/UIKit.h>
#import "KSScreenshotManager.h"

@class MyTableViewController;

@interface MyScreenshotManager : KSScreenshotManager

@property(nonatomic, strong) MyTableViewController *tableViewController;

@end

#endif
