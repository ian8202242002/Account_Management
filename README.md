## HTTP APIs for Account and Password Management

實作帳號管理

### step 1 - git clone repo
```
git clone https://github.com/ian8202242002/Account_Management.git
```

### step 2 - Build docker image with Dockerfile

```
docker image build -t account_management .
```

### step 3 - Run docker image

```
docker run -p 80:8888 account_management
```

連線 http://0.0.0.0:80/api/ 或 http://127.0.0.1:80/api/ , 就可以看到 Account management api doc with swagger, 可以在 swagger UI 上進行 api 的操作
