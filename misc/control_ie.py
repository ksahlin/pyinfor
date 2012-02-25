import IEC

""" To control Internet Explorer

http://www.mayukhbose.com/python/IEC/index.php
"""

ie = IEC.IEController()                  # Create a new IE Window.
ie.Navigate('http://www.google.com/')    # Navigate to a website.
# find "<input autocomplete=off maxlength=2048 name=q"
ie.SetInputValue('q', 'Xiao Jianfeng')     # Fill in the search box.
ie.ClickButton(caption='Google Search')  # Click on the search button.
ie.ClickLink(linktext="Xiao Jianfeng | Linkedin")


ie = IEC.IEController()                  # Create a new IE Window.
ie.Navigate('http://www.google.com/')    # Navigate to a website.
# find "<input autocomplete=off maxlength=2048 name=q"
ie.SetInputValue('q', 'Xiao Jianfeng')     # Fill in the search box.
ie.ClickButton(caption='Google Search')  # Click on the search button.
ie.ClickLink("Xiao Jianfeng | Linkedin")
#ie.SetInputValue("firstName", "xiaojf")
ie.ClickLink("Sign In")
ie.SetInputValue("session_key", "xiaojianfeng@gmail.com")
ie.SetInputValue("session_password", "MY_PASSWORD")
ie.ClickButton(caption="Sign In")
if "Welcome" in ie.GetDocumentText():
    print "Done!"
else:
    print "ERROR!"
