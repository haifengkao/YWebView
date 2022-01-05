// swift-tools-version:5.5
// The swift-tools-version declares the minimum version of Swift required to build this package.
// manual build: swift build -Xswiftc "-sdk" -Xswiftc "/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneSimulator.platform/Developer/SDKs/iPhoneSimulator13.0.sdk" -Xswiftc "-target" -Xswiftc "x86_64-apple-ios12.1-simulator"
import PackageDescription

let package = Package(
    name: "YWebView",
    platforms: [
        .macOS(.v10_10),
        .iOS(.v8),
    ],
    products: [
        // Products define the executables and libraries produced by a package, and make them visible to other packages.
        .library(
            name: "YWebView",
            targets: ["YWebView"]
        ),
    ],
    dependencies: [
        // Dependencies declare other packages that this package depends on.
        // .package(url: /* package url */, from: "1.0.0"),
        .package(url: "https://github.com/Quick/Quick.git", from: "4.0.0"),
        .package(url: "https://github.com/Quick/Nimble.git", from: "9.0.0"),
    ],
    targets: [
        // Targets are the basic building blocks of a package. A target can define a module or a test suite.
        // Targets can depend on other targets in this package, and on products in packages which this package depends on.
        .target(
            name: "YWebView",
            dependencies: [],
            path: "Sources",
            publicHeadersPath: "Include"
        ),
        // .target(
        //     name: "YWebViewExample",
        //     dependencies: ["YWebView"],
        //     path: "Example/Shared"
        // ),
        .testTarget(
            name: "YWebViewTests",
            dependencies: [
                "YWebView",
                "Quick",
                "Nimble",
            ]
        ),
    ]
)
