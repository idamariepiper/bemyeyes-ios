//
//  BMEConstants.h
//  BeMyEyes
//
//  Created by Marcin Kuptel on 30/01/15.
//  Copyright (c) 2015 Be My Eyes. All rights reserved.
//

#ifndef BeMyEyes_BMEConstants_h
#define BeMyEyes_BMEConstants_h

#define BMEAPIPublicBaseUrl @"https://api.bemyeyes.org"
#define BMEAPIStagingBaseUrl @"https://stagingapi.bemyeyes.org"
#define BMEAPIDevelopmentBaseUrl @"https://devapi.bemyeyes.org"

#define BMEBundleIdProduction @"org.bemyeyes.BeMyEyes"
#define BMEBundleIdStaging @"org.bemyeyes.BeMyEyes.staging"
#define BMEBundleIdDevelopment @"org.bemyeyes.BeMyEyes.dev"

#define BMEFeedbackRecipientEmail @"info@bemyeyes.org"
#define BMEBetaFeedbackRecipientEmail @"beta@bemyeyes.org"
#define BMEFeedbackEmailSubject @"Feedback on Be My Eyes"

#define BMEPeopleHelpedBeforeAskingForMoreLanguages 3

#define BMEErrorDomain @"org.bemyeyes.BeMyEyes"

#define BMEFrontPageNavigationControllerIdentifier @"FrontPageNavigation"
#define BMEFrontPageControllerIdentifier @"FrontPage"
#define BMEMainNavigationControllerIdentifier @"MainNavigation"
#define BMEMainBlindControllerIdentifier @"MainBlind"
#define BMEMainHelperControllerIdentifier @"MainHelper"
#define BMEMenuControllerIdentifier @"Menu"
#define BMECallControllerIdentifier @"Call"
#define BMESecretSettingsControllerIdentifier @"SecretSettings"
#define BMEForgotPasswordControllerIdentifier @"ForgotPassword"
#define BMEDemoCallViewController @"DemoCall"
#define BMEHelperWelcomeViewController @"HelperWelcome"

#define BMEDidLogInNotification @"BMEDidLogInNotification"
#define BMEDidLogOutNotification @"BMEDidLogOutNotification"
#define BMEDidUpdateProfileNotification @"BMEDidUpdateProfileNotification"
#define BMEDidUpdatePointNotification @"BMEDidUpdatePointNotification"
#define BMEGoToLoginIfPossibleNotification @"BMEGoToLoginIfPossibleNotification"
#define BMEInitiateCallIfPossibleNotification @"BMEInitateCallIfPossibleNotification"
#define BMEDidAnswerDemoCallNotification @"BMEDidAnswerDemoCallNotification"
#define BMEDidRegisterUserNotificationsNotification @"BMEDidRegisterUserNotificationsNotification"

#define BMEDidLogInNotificationDisplayHelperWelcomeKey @"BMEDidLogInNotificationDisplayHelperWelcomeKey"

#define NotificationCategoryReply @"REPLY_ACTIONABLE"
#define NotificationActionReplyNo @"ACTION_RESPOND_NO"
#define NotificationActionReplyYes @"ACTION_RESPOND_YES"

#endif
