//
//  YViewController.m
//  YWebView
//
//  Created by Hai Feng Kao on 06/25/2016.
//  Copyright (c) 2016 Hai Feng Kao. All rights reserved.
//

#import "YViewController.h"
#import "YWebView.h"

@interface YViewController ()
@property (nonatomic, weak) YWebView* webView;
@end

@implementation YViewController

- (void)viewDidLoad
{
    [super viewDidLoad];
    // Do any additional setup after loading the view, typically from a nib.
    YWebView* webView = [[YWebView alloc] initWithFrame:self.view.bounds configuration:nil];
    NSURL* url = [NSURL URLWithString:@"http://www.google.com"];
    NSURLRequest* request = [NSURLRequest requestWithURL:url];
    [webView loadRequest:request];
    self.webView = webView;
    
    [self.view addSubview:webView];
}

- (void)didReceiveMemoryWarning
{
    [super didReceiveMemoryWarning];
    // Dispose of any resources that can be recreated.
}

@end
