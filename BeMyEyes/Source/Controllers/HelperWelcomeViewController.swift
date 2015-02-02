//
//  HelperWelcomeViewController.swift
//  BeMyEyes
//
//  Created by Simon Støvring on 29/01/15.
//  Copyright (c) 2015 Be My Eyes. All rights reserved.
//

import UIKit

class HelperWelcomeViewController: UIViewController {

    @IBOutlet weak var titleLabel: UILabel!
    @IBOutlet weak var descriptionLabel: UILabel!
    @IBOutlet weak var demoCallButton: Button!
    @IBOutlet weak var doneButton: Button!
    @IBOutlet weak var heartImageView: UIImageView!
    
    // MARK: - Lifecycle
    
    override func viewDidLoad() {
        super.viewDidLoad()
        
        heartImageView.tintColor = .whiteColor()
        doneButton.mainStyle = .Border
        
        let firstName = BMEClient.sharedClient().currentUser.firstName
        titleLabel.text = NSString(format: MKLocalizedFromTable("BME_HELPER_WELCOME_TITLE", "HelperWelcomeLocalizationTable"), firstName)
        descriptionLabel.text = MKLocalizedFromTable("BME_HELPER_WELCOME_DESCRIPTION", "HelperWelcomeLocalizationTable")
        demoCallButton.title = MKLocalizedFromTable("BME_HELPER_DEMO_CALL_TITLE", "HelperWelcomeLocalizationTable")
        doneButton.title = MKLocalizedFromTable("BME_HELPER_DONE_TITLE", "HelperWelcomeLocalizationTable")
    }
    
    override func preferredStatusBarStyle() -> UIStatusBarStyle {
        return .LightContent
    }
    
    // MARK: - Private methods

    @IBAction func demoCallButtonPressed(sender: AnyObject) {
        let controller = storyboard?.instantiateViewControllerWithIdentifier(BMEDemoCallViewController) as DemoCallViewController
        controller.callCompletion = { controller in
            self.dismissViewControllerAnimated(true, completion: nil)
        }
        
        presentViewController(controller, animated: true, completion: nil)
    }
    
    @IBAction func doneButtonPressed(sender: AnyObject) {
        dismissViewControllerAnimated(true, completion: nil)
    }
}
