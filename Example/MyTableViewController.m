//
//  MyTableViewController.m
//  KSScreenshotManagerExample
//
//  Created by Kent Sutherland on 2/10/13.
//  Copyright (c) 2013 Kent Sutherland. All rights reserved.
//

#import "MyTableViewController.h"

@interface MyTableViewController ()

@end

@implementation MyTableViewController

- (void)viewDidLoad
{
    [super viewDidLoad];
    
    [[self tableView] registerClass:[UITableViewCell class] forCellReuseIdentifier:@"Cell"];
}

- (void)didReceiveMemoryWarning
{
    [super didReceiveMemoryWarning];
}

#pragma mark - Table View Data Source & Delegate

- (NSInteger)numberOfSectionsInTableView:(UITableView *)tableView
{
    return 1;
}

- (NSInteger)tableView:(UITableView *)tableView numberOfRowsInSection:(NSInteger)section
{
    return 40;
}

- (UITableViewCell *)tableView:(UITableView *)tableView cellForRowAtIndexPath:(NSIndexPath *)indexPath
{
    static NSString *CellIdentifier = @"Cell";
    UITableViewCell *cell = [tableView dequeueReusableCellWithIdentifier:CellIdentifier forIndexPath:indexPath];
    
    [[cell textLabel] setText:[NSString stringWithFormat:NSLocalizedString(@"English Cell %1$d", nil), [indexPath row] + 1]];
    
    return cell;
}

@end
