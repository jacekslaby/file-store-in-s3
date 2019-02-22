Feature: Querying for stored files

  Background: There are six domains with files: Shell, BP-upstream, BP-midstream, BP-downstream, AL, CA
       Given There are two files in domain Shell
         And There are four files in domain BP-upstream
         And There are ten files in domain BP-downstream
         And There are zero files in domain BP-midstream
         And There are three files in domain AL
         And There are two files in domain CA

  Scenario: User Dutchman from Shell lists available files
      When I query for files from domain matching regexp 'Shell'
      Then I receive two files from domain Shell
       And I receive no other files

  Scenario: User Greenwood from BP lists available files
      When I query for files from domain matching regexp 'BP.*'
      Then I receive four files from domain BP-upstream
       And I receive ten files from domain BP-downstream
       And I receive no other files

  Scenario: User Maria has access to Shell, BP and AL and lists available files
      When I query for files from domain matching regexp 'Shell|BP.*|AL'
      Then I receive two files from domain Shell
       And I receive four files from domain BP-upstream
       And I receive ten files from domain BP-downstream
       And I receive three files from domain AL
       And I receive no other files

  Scenario: User Nobody has no access and lists available files
      When I query for files from domain matching regexp ''
      Then I receive no other files
