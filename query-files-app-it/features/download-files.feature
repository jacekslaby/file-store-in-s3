Feature: Downloading stored files

  Background: There are six domains with files: Shell, BP-upstream, BP-midstream, BP-downstream, AL, CA
       Given There are "2" files in domain "Shell"
         And There are "4" files in domain "BP-upstream"
         And There are "10" files in domain "BP-downstream"
         And There are "0" files in domain "BP-midstream"
         And There are "3" files in domain "AL"
         And There are "2" files in domain "CA"

  Scenario: User Dutchman from Shell downloads a file
      When I query for files from domain matching regexp "Shell"
       And I download "1" files from domain "Shell"
      Then I receive files contents

  Scenario: User Greenwood from BP downloads several files
      When I query for files from domain matching regexp "BP.*"
       And I download "2" files from domain "BP-upstream"
       And I download "3" files from domain "BP-downstream"
      Then I receive files contents

  Scenario: User Greenwood from BP cannot download files from Shell
      When I query for files from domain matching regexp "BP.*"
       And I download "1" files from domain "Shell"
      Then I receive no such file error

  Scenario: User Nobody has no access and cannot download file from Shell
      When I query for files from domain matching regexp " "
       And I download "1" files from domain "Shell"
      Then I receive no such file error
