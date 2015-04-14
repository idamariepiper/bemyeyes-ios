module Fastlane
  module Actions
    module SharedValues
      CROWDIN_PROJECT_KEY_CUSTOM_VALUE = :CROWDIN_PROJECT_KEY_CUSTOM_VALUE
    end

    class CrowdinProjectKeyAction < Action
      def self.run(params)
        Actions.lane_context[SharedValues::CROWDIN_PROJECT_KEY_CUSTOM_VALUE] = projectKey()
      end



      #####################################################
      # @!group Documentation
      #####################################################

      def self.description
        "Finds the CrowdIn project key in BMEGlobale.h"
      end

      def self.available_options
        # Define all options your action supports. 
        # The environment variable (last parameters) is optional, remove it if you don't need it
        # You can add as many parameters as you want
        # [
        #   ['path', 'Describe what this parameter is useful for', 'ENVIRONMENT_VARIABLE_NAME'],
        #   ['second', 'Describe what this parameter is useful for']
        # ]
      end

      def self.output
        # Define the shared values you are going to provide
        # Example
        [
          ['CROWDIN_PROJECT_KEY_CUSTOM_VALUE', 'A description of what this value contains']
        ]
      end

      def self.author
        # So no one will ever forget your contribution to fastlane :) You are awesome btw!
        'duemunk'
      end
      
      def self.projectKey
        projectKey = ''
        filename = "./BeMyEyes/Source/BMEGlobal.h"
        File.open(filename, "r:UTF-8") do |f|
          contents = f.read
          contents.scan(/\#define\s([^\s]*)\s@\"([^\"]*)\"/) do |key, value|
            if key == "BMECrowdInProjectKey"
              projectKey = value
            end
          end
        end
        return projectKey
      end
    end
  end
end