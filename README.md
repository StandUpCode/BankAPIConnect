# BankAPIConnect

### SCB & KBank API Connect

[SCB Doc](https://developer.scb/#/documents/documentation/basics/getting-started.html)

[KBank Doc](https://apiportal.kasikornbank.com/product)

### This Projects Use [pyzbar](https://pypi.org/project/pyzbar/) for detect and decode QRCode


---
####  To RUN
```shell
docker-compose -f prod.docker-compose.yml up -d
```

**Note For Developer**
- For SCB API Slip Verification can 
verify only transaction that was create via sandbox and SCBEasy Simulator 
- Real transaction can't Use with sandbox api

----
## To Contribute
- Fork this repository
- Write your code (pls follow the name convention)
- Create the pull request
----
### License 
MIT

---
Special Thanks [codustry](https://github.com/codustry)

- https://github.com/codustry/thanakan [Thai Bank API Interface]