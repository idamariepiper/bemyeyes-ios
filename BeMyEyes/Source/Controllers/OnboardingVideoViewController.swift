//
//  OnboardingVideoViewController.swift
//  BeMyEyes
//
//  Created by Tobias DM on 07/10/14.
//  Copyright (c) 2014 Be My Eyes. All rights reserved.
//

import UIKit

class OnboardingVideoViewController: IntroVideoViewController {

    let videoToSignUpSegue = "VideoToSignUp"
    var role: BMERole?
	
	override func viewDidLoad() {
		super.viewDidLoad()
		
		if let movieView = moviePlayerController.view {
			if let doneButton = doneButton {
				view.insertSubview(movieView, belowSubview: doneButton)
			}
		}
	}
	
    override func finishedPlaying() {
        super.finishedPlaying()
        
        self.performSegueWithIdentifier(videoToSignUpSegue, sender: self)
    }
    
    override func prepareForSegue(segue: UIStoryboardSegue, sender: AnyObject?) {
        if segue.identifier == videoToSignUpSegue {
            if let signup = segue.destinationViewController as? BMESignUpMethodViewController {
                if let role = role {
                    signup.role = role
                }
            }
        }
    }
    
    @objc internal func setHelperRole() {
        role = .Helper
    }
    
    @objc internal func setBlindRole() {
        role = .Blind
    }
    
}