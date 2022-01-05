//
//  ContentView.swift
//  Shared
//
//  Created by Hai Feng Kao on 01/05/2022.
//

import SwiftUI
import YWebView

struct YWebViewUI: UIViewRepresentable {
    @Binding var request: URLRequest

    func makeUIView(context _: Context) -> YWebView {
        YWebView()
    }

    func updateUIView(_ uiView: YWebView, context _: Context) {
        uiView.load(request)
    }
}

struct ContentView: View {
    @State var request: URLRequest = .init(url: URL(string: "https://www.google.com")!)
    var body: some View {
        YWebViewUI(request: $request)
    }
}

struct ContentView_Previews: PreviewProvider {
    static var previews: some View {
        ContentView()
    }
}
