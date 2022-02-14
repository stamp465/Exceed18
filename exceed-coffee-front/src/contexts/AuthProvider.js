import React, { createContext, useContext, useEffect, useState } from "react"
import { useNavigate } from "react-router-dom"

const AuthContext = createContext({})

const AuthProvider = ({ children }) => {
  const [user, setUser] = useState({})
  const [token, setToken] = useState({})

  const navigate = useNavigate()

  const setUserInfo = (user, token) => {
    //localStorage.setItem("user", JSON.stringify(user))
    localStorage.setItem("access_token", JSON.stringify(token))
    //setUser(user)
    navigate("/dashboard")
  }

  const logout = () => {
    //localStorage.removeItem("user")
    localStorage.removeItem("access_token")
    //setUser({})
    setToken({})
    navigate("/home")
  }

  useEffect(() => {
    //const oldUser = localStorage.getItem("user")
    const oldUser_token = localStorage.getItem("access_token")
    if (oldUser_token) {//oldUser &&
      navigate("/dashboard")
      //setUser(JSON.parse(oldUser))
      setToken(JSON.parse(oldUser_token))
    } else {
      // navigate("/login")
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [])

  return (
    <AuthContext.Provider value={{ user, token, setUserInfo, logout }}>
      {children}
    </AuthContext.Provider>
  )
}

export const useAuth = () => useContext(AuthContext)

export default AuthProvider