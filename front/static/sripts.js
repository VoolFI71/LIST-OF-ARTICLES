function getJwtTokenFromCookie() {
    const cookieName = "jwt";
    const cookieValue = document.cookie.split('; ').find(row => row.startsWith(cookieName + '='));

    if (cookieValue) {
      return cookieValue.split('=')[1];
    } else {
      return null;
    }
  }

  const jwtToken = getJwtTokenFromCookie();

if (jwtToken) {
  console.log("JWT Token:", jwtToken);
} else {
  console.log("JWT Token not found in cookies.");
}