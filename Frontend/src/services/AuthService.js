import axios from 'axios';
import { jwtDecode } from 'jwt-decode';
import CryptoJS, { MD5 } from 'crypto-js';
import NotificationService from './NotificationService';

class AuthService {
  login(username, password, rememberMe) {
    // 对密码进行SHA-256哈希处理
    const hashedPassword = MD5(password).toString();
  
    return axios
      .post(`${import.meta.env.VITE_APP_API_URL}/login`, {
        username,
        password: hashedPassword,
        rememberMe
      })
      .then(response => {
        if (response.data.access_token) {
          localStorage.setItem('access_token', response.data.access_token);
        }
        return response.data;
      });
  }

  logout() {
    localStorage.removeItem('access_token');
  }

  getToken() {
    return localStorage.getItem('access_token');
  }

  isAuthenticated() {
    const token = this.getToken();
    if (!token) {
      return false;
    }
    
    try {
      const decoded = jwtDecode(token);
      const currentTime = Date.now() / 1000;
      if (decoded.exp < currentTime) {
        NotificationService.notify('Session expired, please login again', 'error');
        this.logout();
        return false;
      }
      return true;
    } catch (error) {
      return false;
    }
  }


  getUserInfo() {
    const token = this.getToken();
    if (!token) return null;
    
    try {
      // 解码JWT获取用户信息
      const decoded = jwtDecode(token);
      return decoded;
    } catch (error) {
      console.error('解码token失败:', error);
      return null;
    }
  }

  getUsername() {
    const userInfo = this.getUserInfo();
    return userInfo ? userInfo.sub : null;
  }

  getUserAvatar() {
    const userInfo = this.getUserInfo();
    console.log(userInfo);
    console.log(userInfo.avatar);
    return userInfo ? userInfo.avatar : null;
  }
}

export default new AuthService();