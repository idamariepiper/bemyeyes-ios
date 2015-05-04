//
//  UserTokenHandler.swift
//  BeMyEyes
//
//  Created by Tobias Due Munk on 04/05/15.
//  Copyright (c) 2015 Be My Eyes. All rights reserved.
//

import Foundation

let keychain = Keychain(service: NSBundle.mainBundle().bundleIdentifier ?? "org.bemyeyes.Be-My-Eyes").synchronizable(true)

class UserTokenHandler: NSObject {
    
    class func uniqueToken() -> String {
        if let token = keychain[BMEKeychainToken] {
            return token
        }
        let token = newToken()
        keychain[BMEKeychainToken] = token
        return token
    }
    
    private class func newToken() -> String {
        return NSUUID().UUIDString
    }
}
