# YWebView

[![CI Status](http://img.shields.io/travis/haifengkao/YWebView.svg?style=flat)](https://travis-ci.org/haifengkao/YWebView)
[![Coverage Status](https://coveralls.io/repos/haifengkao/YWebView/badge.svg?branch=master&service=github)](https://coveralls.io/github/haifengkao/YWebView?branch=master)
[![Version](https://img.shields.io/cocoapods/v/YWebView.svg?style=flat)](http://cocoapods.org/pods/YWebView)
[![License](https://img.shields.io/cocoapods/l/YWebView.svg?style=flat)](http://cocoapods.org/pods/YWebView)
[![Platform](https://img.shields.io/cocoapods/p/YWebView.svg?style=flat)](http://cocoapods.org/pods/YWebView)

The primary codes are copied from an answer of [SO](http://stackoverflow.com/a/32845148/912645).
All cookies will be loaded from `NSHTTPCookieStorage`. When a web page is loaded, its cookies will be save to NSHTTPCookieStorage as well.
This method allows cookie sharing among multiple WKWebView and UIWebView.

If you want to remove all cookies, use
```objc
NSHTTPCookieStorage *cookieStorage = [NSHTTPCookieStorage sharedHTTPCookieStorage];
for (NSHTTPCookie *cookie in cookieStorage.cookies) {
    [cookieStorage deleteCookie:cookie];
}
```

## Usage
Just use YWebView as the ordinary WKWebView.

## Example

To run the example project, clone the repo, and run `pod install` from the Example directory first.

## Requirements
iOS 8.0 (the minimum requirement for WKWebView)

## Installation

YWebView is available through [CocoaPods](http://cocoapods.org). To install
it, simply add the following line to your Podfile:

```ruby
pod "YWebView"
```

## Author

Hai Feng Kao, haifeng@cocoaspice.in

## License

YWebView is available under the MIT license. See the LICENSE file for more info.
