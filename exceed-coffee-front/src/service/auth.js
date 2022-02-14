import axios from "axios"

export async function login(user) {
  var str = [];
  for (var key in user) {
    if (user.hasOwnProperty(key)) {
      str.push(encodeURIComponent(key) + "=" + encodeURIComponent(user[key]))
      console.log(key + " -> " + user[key]);
    }
  }
  str = str.join("&");
  const res = await axios.post("http://127.0.0.1:8000/token", str)
  console.log(str)
  return res.data
}

//dsa