//
//  YWebView.h
//  YWebView
//
//  Created by Hai Feng Kao on 2016/06/25.
//
//

#import <Foundation/Foundation.h>
#import <WebKit/WebKit.h>

@interface YWebView : WKWebView

- (instancetype)initWithFrame:(CGRect)frame configuration:(WKWebViewConfiguration*)theConfiguration NS_DESIGNATED_INITIALIZER;
- (WKNavigation*)loadRequest:(NSURLRequest*)request;
@end
