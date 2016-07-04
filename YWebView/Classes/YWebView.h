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

// workaround http://stackoverflow.com/questions/31094110/memory-leak-when-using-wkscriptmessagehandler
// put the message handler name here, YWebView will remove them when dealloc
- (void)addScriptMessageHandlerNameForCleanup:(NSString*)name;
@end
