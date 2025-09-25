## 🚀 FastAPI JWT Authentication Study

This project explores **JWT authentication** with [FastAPI](https://fastapi.tiangolo.com/).  
It combines insights from:

-   📺 [Tutorial Video](https://www.youtube.com/watch?v=KxR3OONvDvo)
-   📚 [Official Documentation](https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/#hash-and-verify-the-passwords)

Additionally, it demonstrates best practices for project structure.  
Enjoy learning and building secure APIs! 🔒✨

---

## 🛠️ Step-by-Step Guide to Run the Project

1. **📦 Install dependencies**

    ```bash
    pip install -r requirements.txt
    ```

2. **🚀 Start the FastAPI server**

    ```bash
    uvicorn main:app --reload
    ```

    or

    ```bash
    fastapi dev app/main.py
    ```

3. **🌐 Prepare**

    - Copy the `template.env` file to `.env` and fill in all required environment variables as instructed in the file.

4. **🌐 Acess the API docs**

    - Open your browser and go to: [http://localhost:8000/docs](http://localhost:8000/docs)

5. **🔑 Test JWT Authentication**

    - Use the `/login` endpoint to obtain a JWT token.
    - Authorize requests by clicking "Authorize" in the Swagger UI and pasting your token.

6. **✅ Explore secured endpoints**
    - Try accessing protected routes to verify authentication.

---

> 💡 **Tip:** Make sure you have Python 3.10+ installed before starting.
