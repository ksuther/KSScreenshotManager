//
//  AppDelegate.m
//  KSScreenshotManagerExample
//
//  Created by Kent Sutherland on 2/10/13.
//  Copyright (c) 2013 Kent Sutherland. All rights reserved.
//

#import "AppDelegate.h"
#import "MyTableViewController.h"

#if CREATING_SCREENSHOTS
    #import "MyScreenshotManager.h"
#endif

@implementation AppDelegate

- (BOOL)application:(UIApplication *)application didFinishLaunchingWithOptions:(NSDictionary *)launchOptions
{
    self.window = [[UIWindow alloc] initWithFrame:[[UIScreen mainScreen] bounds]];
    // Override point for customization after application launch.
    self.window.backgroundColor = [UIColor whiteColor];
    [self.window makeKeyAndVisible];
    
    MyTableViewController *viewController = [[MyTableViewController alloc] initWithStyle:UITableViewStylePlain];
    
    self.window.rootViewController = viewController;
    
#if CREATING_SCREENSHOTS
    dispatch_time_t popTime = dispatch_time(DISPATCH_TIME_NOW, (int64_t)(2.0 * NSEC_PER_SEC));
    dispatch_after(popTime, dispatch_get_main_queue(), ^(void){
        MyScreenshotManager *screenshotManager = [[MyScreenshotManager alloc] init];
        
        [screenshotManager setTableViewController:viewController];
        [screenshotManager takeScreenshots];
    });
#endif
    
    return YES;
}

@end
