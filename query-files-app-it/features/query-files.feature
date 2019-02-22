Feature: Querying for stored files

  Background: There are six domains with files: Shell, BP-upstream, BP-midstream, BP-downstream, AL, CA
       Given There are "2" files in domain "Shell"
         And There are "4" files in domain "BP-upstream"
         And There are "10" files in domain "BP-downstream"
         And There are "0" files in domain "BP-midstream"
         And There are "3" files in domain "AL"
         And There are "2" files in domain "CA"

  Scenario: User Dutchman from Shell lists available files
      When I query for files from domain matching regexp "Shell"
      Then I receive "2" files from domain "Shell"
       And I receive no other files

  Scenario: User Greenwood from BP lists available files
      When I query for files from domain matching regexp "BP.*"
      Then I receive "4" files from domain "BP-upstream"
       And I receive "10" files from domain "BP-downstream"
       And I receive no other files

  Scenario: User Maria has access to Shell, BP and AL and lists available files
      When I query for files from domain matching regexp "Shell|BP.*|AL"
      Then I receive "2" files from domain "Shell"
       And I receive "4" files from domain "BP-upstream"
       And I receive "10" files from domain "BP-downstream"
       And I receive "3" files from domain "AL"
       And I receive no other files

  Scenario: User Nobody has no access and lists available files
      When I query for files from domain matching regexp " "
      Then I receive no other files
