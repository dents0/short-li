# Short-Li
A **URL shortener** using Flask on GAE standard and Cloud SQL for PostgreSQL.

**Link:** [https://short-li.com][1] \
**Author:** Deniss Tsokarev

---

### How it works
1. The form takes a URL checking its format using 
    [url_filter.py][2].
2. If the URL format is valid, the app checks if the URL is already stored inside the database and if it is - returns 
    the shortened URL for it.
3. If there is no such URL stored in the database, the app assigns it a unique ID and adds both to the database.
4. The app returns the domain name with the ID for that URL as an endpoint - e.g. 
    "**short-li.com/URL_ID**".
5. If you go to the shortened URL, the app will look up the original URL value in the database searching for it by 
    the ID provided in the endpoint. Once the original URL is found, you will be redirected to it.

---

  [1]: https://short-li.com
  [2]: https://github.com/dents0/short-li/blob/main/url_shortener/url_filter.py
