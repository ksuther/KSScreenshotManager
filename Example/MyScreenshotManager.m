//
//  MyScreenshotManager.m
//  KSScreenshotManagerExample
//
//  Created by Kent Sutherland on 2/10/13.
//  Copyright (c) 2013 Kent Sutherland. All rights reserved.
//

#if CREATING_SCREENSHOTS

#import "MyScreenshotManager.h"
#import "KSScreenshotAction.h"
#import "MyTableViewController.h"

//Private API to programmatically force the simulator into a different orientation
//Don't ship this to the App Store!
@interface UIDevice ()
- (void)setOrientation:(UIInterfaceOrientation)orientation;
@end

@implementation MyScreenshotManager

- (void)setupScreenshotActions
{
    //Two contrived screenshot actions
    //Scroll the table view to a different row and take a screenshot
    
    //Create a synchronous action
    //This means the screenshot will automatically be taken after running the actionBlock (after running the run loop to allow view to lay out)
    KSScreenshotAction *synchronousAction = [KSScreenshotAction actionWithName:@"tableView1" asynchronous:NO actionBlock:^{
        NSIndexPath *indexPath = [NSIndexPath indexPathForRow:2 inSection:0];
        
        [[[self tableViewController] tableView] scrollToRowAtIndexPath:indexPath atScrollPosition:UITableViewScrollPositionTop animated:NO];
    } cleanupBlock:^{
        [[[self tableViewController] tableView] setContentOffset:CGPointZero];
    }];
    
    [self addScreenshotAction:synchronousAction];
    
    //Create an asynchronous action
    //This is a pretty contrived example, but it shows how -actionIsReady is used
    KSScreenshotAction *asynchronousAction = [KSScreenshotAction actionWithName:@"tableView2" asynchronous:YES actionBlock:^{
        NSIndexPath *indexPath = [NSIndexPath indexPathForRow:8 inSection:0];
        
        [[[self tableViewController] tableView] scrollToRowAtIndexPath:indexPath atScrollPosition:UITableViewScrollPositionTop animated:NO];
        
        [[UIDevice currentDevice] setOrientation:UIInterfaceOrientationLandscapeLeft]; //programmatically switch to landscape (private API)
        
        dispatch_time_t popTime = dispatch_time(DISPATCH_TIME_NOW, (int64_t)(2.0 * NSEC_PER_SEC));
        dispatch_after(popTime, dispatch_get_main_queue(), ^(void){
            [self actionIsReady];
        });
    } cleanupBlock:nil];
    
    [self addScreenshotAction:asynchronousAction];
}

@end

#endif
