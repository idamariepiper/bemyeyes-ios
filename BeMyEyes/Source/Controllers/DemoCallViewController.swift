//
//  DemoCallViewController.swift
//  BeMyEyes
//
//  Created by Simon Støvring on 22/01/15.
//  Copyright (c) 2015 Be My Eyes. All rights reserved.
//

import UIKit

class DemoCallViewController: BMEBaseViewController {

	let DemoVideoSegue = "DemoVideo"
	let DemoCallFireNotificationAfterSeconds: NSTimeInterval = 2
	
	@IBOutlet weak var titleLabel: UILabel!
	@IBOutlet weak var cancelButton: UIButton!
	@IBOutlet weak var step1Label: UILabel!
	@IBOutlet weak var step2Label: UILabel!
    @IBOutlet weak var step3Label: UILabel!
	@IBOutlet weak var stepsView: UIView!
	@IBOutlet weak var enableNotificationsLabel: UILabel!
	
    internal var callCompletion: ((UIViewController) -> ())?
	
	private var canPerformDemoCall: Bool {
		if UIApplication.instancesRespondToSelector(Selector("registerUserNotificationSettings:")) {
			let application = UIApplication.sharedApplication()
			let types = application.currentUserNotificationSettings().types.rawValue
			let soundEnabled = types & UIRemoteNotificationType.Sound.rawValue != 0
			let alertEnabled = types & UIRemoteNotificationType.Alert.rawValue != 0
			let badgeEnabled = types & UIRemoteNotificationType.Badge.rawValue != 0
			return application.isRegisteredForRemoteNotifications() && soundEnabled && alertEnabled && badgeEnabled
		}
		return true
	}
	
	// MARK: - Lifecycle
	
    override func viewDidLoad() {
        super.viewDidLoad()
		
		MKLocalization.registerForLocalization(self)
		
		receiveDidEnterBackgroundNotifications(true)
		NSNotificationCenter.defaultCenter().addObserver(self, selector: Selector("didAnswerDemoCall:"), name: BMEDidAnswerDemoCallNotification, object: nil)
		NSNotificationCenter.defaultCenter().addObserver(self, selector: Selector("didRegisterUserNotificationsNotification:"), name: BMEDidRegisterUserNotificationsNotification, object: nil)
		
		checkIfDemoCallCanBePerformed()
    }
	
	deinit {
		NSNotificationCenter.defaultCenter().removeObserver(self)
		UIApplication.sharedApplication().cancelAllLocalNotifications()
	}
	
	// MARK: - Public methods
	
	class func NotificationIsDemoKey() -> String {
		return "BMEIsDemo"
	}
	
	// MARK: - Private methods
	
	@IBAction func cancelButtonPressed(sender: AnyObject) {
		dismissViewControllerAnimated(true, completion: nil)
	}
	
	private func checkIfDemoCallCanBePerformed() {
		updateDisplayedViews()
		
		if !canPerformDemoCall {
			let settings = UIUserNotificationSettings(forTypes: .Sound | .Alert | .Badge, categories: BMEAccessControlHandler.notificationCategories())
			UIApplication.sharedApplication().registerUserNotificationSettings(settings)
		}
	}
	
	private func updateDisplayedViews() {
		stepsView.hidden = !canPerformDemoCall
		enableNotificationsLabel.hidden = canPerformDemoCall
	}
	
	internal func didEnterBackground(notification: NSNotification) {
		receiveWillEnterForegroundNotifications(true)
		receiveDidEnterBackgroundNotifications(false)
		
		if canPerformDemoCall {
			let blindName = MKLocalizedFromTable("POST_CALL_VIEW_CONTROLLER_BLIND_NAME", "DemoCallLocalizationTable")
			let fireDate = NSDate().dateByAddingTimeInterval(DemoCallFireNotificationAfterSeconds)
			let notification = UILocalNotification()
			notification.fireDate = fireDate
			notification.alertBody = NSString(format: MKLocalized("PUSH_NOTIFICATION_ANSWER_REQUEST_MESSAGE"), blindName)
			notification.userInfo = [DemoCallViewController.NotificationIsDemoKey() : true]
			notification.soundName = "call-repeat.aiff"
			notification.applicationIconBadgeNumber = 0
            notification.category = NotificationCategoryReply;
			UIApplication.sharedApplication().scheduleLocalNotification(notification)
		}
	}
	
	internal func willEnterForeground(notification: NSNotification) {
		receiveWillEnterForegroundNotifications(false)
		receiveDidEnterBackgroundNotifications(true)
		UIApplication.sharedApplication().cancelAllLocalNotifications()
		checkIfDemoCallCanBePerformed()
	}
	
	internal func didAnswerDemoCall(notification: NSNotification) {
		receiveDidEnterBackgroundNotifications(false)
		performSegueWithIdentifier(DemoVideoSegue, sender: nil)
	}
	
	internal func didRegisterUserNotificationsNotification(notification: NSNotification) {
		updateDisplayedViews()
	}
	
	private func receiveDidEnterBackgroundNotifications(receive: Bool) {
		if receive {
			NSNotificationCenter.defaultCenter().addObserver(self, selector: Selector("didEnterBackground:"), name: UIApplicationDidEnterBackgroundNotification, object: nil)
		} else {
			NSNotificationCenter.defaultCenter().removeObserver(self, name: UIApplicationDidEnterBackgroundNotification, object: nil)
		}
	}
	
	private func receiveWillEnterForegroundNotifications(receive: Bool) {
		if receive {
			NSNotificationCenter.defaultCenter().addObserver(self, selector: Selector("willEnterForeground:"), name: UIApplicationWillEnterForegroundNotification, object: nil)
		} else {
			NSNotificationCenter.defaultCenter().removeObserver(self, name: UIApplicationWillEnterForegroundNotification, object: nil)
		}
	}
    
    override func prepareForSegue(segue: UIStoryboardSegue, sender: AnyObject?) {
        if segue.identifier == DemoVideoSegue {
            let controller = segue.destinationViewController as DemoCallVideoViewController
            controller.completion = callCompletion
        }
    }
}

extension DemoCallViewController: MKLocalizable {
    
    func shouldLocalize() {
        titleLabel.text = MKLocalizedFromTable("POST_CALL_VIEW_CONTROLLER_TITLE", "DemoCallLocalizationTable")
        cancelButton.setTitle(MKLocalizedFromTable("POST_CALL_VIEW_CONTROLLER_CANCEL", "DemoCallLocalizationTable"), forState: .Normal)
        step1Label.text = MKLocalizedFromTable("POST_CALL_VIEW_CONTROLLER_STEP_1", "DemoCallLocalizationTable")
        step2Label.text = MKLocalizedFromTable("POST_CALL_VIEW_CONTROLLER_STEP_2", "DemoCallLocalizationTable")
        step3Label.text = MKLocalizedFromTable("POST_CALL_VIEW_CONTROLLER_STEP_3", "DemoCallLocalizationTable")
        enableNotificationsLabel.text = MKLocalizedFromTable("POST_CALL_VIEW_CONTROLLER_ENABLE_NOTIFICATIONS", "DemoCallLocalizationTable")
    }
}
