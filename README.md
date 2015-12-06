# KSScreenshotManager

Teach your computer to take screenshots of your app so you don't have to anymore. This project simplifies the process of creating automated screenshots of your iOS app. Some assembly is required, as you need to define your screenshots. Once you do that, this code will take care of the rest.

See this blog post for more details: <http://ksuther.com/2013/02/24/automating-ios-app-store-screenshots>

## Adding this to your project

1. Include KSScreenshotManager in your project. Adding it as a submodule is probably the easiest way to do this. Be sure to check out the ios-sim submodule as well by running `git submodule update --init`
1. Add `KSScreenshotManager.h`, `KSScreenshotManager.m`, `KSScreenshotAction.h`, `KSScreenshotAction.m` to your project
1. Subclass `KSScreenshotManager` and override `setupScreenshotActions`
1. Copy config.json.example and customize to suit your project

You can also use [CocoaPods](http://cocoapods.org). You should [create a duplicate target](http://www.codeworth.com/blog/mobile/ios-target-duplication/) in Xcode, so KSScreenshotManager won't be included in your release build. Then, add this to your Podfile:

```ruby
# Replace 'Screenhots Target' with your separate target name
target 'Screenshots Target', :exclusive => true do
  pod 'KSScreenshotManager'
end
```

## Example project

An example project is located in Example (surprise!). It has a very simple KSScreenshotManager subclass named MyScreenshotManager. You can run it with the following command:

`python make_screenshots.py config.json.example`

This will compile the sample project then run the simulator build and dump the screenshots to /tmp/screenshots.

This version does not rely on the `ios-sim` command anymore, instead relying solely on the `simctl` command bundled with Xcode 6 and later. 

## Configuration File

The JSON configuration file now includes references to the simulators enabled on your system. The names in the `device_names` dictionary should match the simulator names as set up in your Xcode devices. The `ios_version` also needs to be set so that simulators can be switched appropriately.

You can get a list of the enabled simulators on the command line by running `xcrun instruments -w help` and using its output to help your populate these configuration values. Note that connected hardware devices will also show up in this list. Run `xcrun simctl list` for a list narrowed down to your simulators.


## License

MIT License

    Copyright (c) 2013 Kent Sutherland
    
    Permission is hereby granted, free of charge, to any person obtaining a copy of
    this software and associated documentation files (the "Software"), to deal in
    the Software without restriction, including without limitation the rights to use,
    copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the
    Software, and to permit persons to whom the Software is furnished to do so,
    subject to the following conditions:
    
    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.
    
    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
    FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
    COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
    IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
    CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
