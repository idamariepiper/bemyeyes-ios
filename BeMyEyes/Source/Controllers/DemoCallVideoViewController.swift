//
//  DemoCallVideoViewController.swift
//  BeMyEyes
//
//  Created by Simon Støvring on 22/01/15.
//  Copyright (c) 2015 Be My Eyes. All rights reserved.
//

import UIKit

class DemoCallVideoViewController: VideoViewController {
	
	@IBOutlet weak var cancelButton: Button!
    internal var completion: ((UIViewController) -> ())?;
	
	// MARK: - Lifecycle
	
	override func viewDidLoad() {
		super.viewDidLoad()
		
        MKLocalization.registerForLocalization(self)
		
		let isIpad = UIDevice.currentDevice().userInterfaceIdiom == .Pad
		moviePlayerController.scalingMode = isIpad ? .AspectFit : .AspectFill
		if let videoPath = NSBundle.mainBundle().pathForResource("demo", ofType: "mp4") {
			let videoUrl = NSURL(fileURLWithPath: videoPath)
			moviePlayerController.contentURL = videoUrl
			moviePlayerController.play()
		}
		
		if let movieView = moviePlayerController.view {
			view.insertSubview(movieView, belowSubview: cancelButton)
		}
	}
	
	override func accessibilityPerformEscape() -> Bool {
		navigationController?.popViewControllerAnimated(false)
		return true
	}
	
	// MARK: - Private methods

	@IBAction func cancelButtonPressed(sender: AnyObject) {
		dismiss()
	}
	
	override func finishedPlaying() {
		super.finishedPlaying()
		
		dismiss()
	}
	
	private func dismiss() {
        if let completion = completion {
            completion(self)
        }
	}
}

extension DemoCallVideoViewController: MKLocalizable {
    func shouldLocalize() {
        cancelButton.title = MKLocalizedFromTable("BME_CALL_DISCONNECT", "BMECallLocalizationTable");
    }
}
