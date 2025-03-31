import axios from 'axios';
import AuthService from './AuthService';

class ApiPrefix {
  constructor() {
    this.api = axios.create({
      baseURL: import.meta.env.VITE_APP_API_URL || 'http://localhost:8080/api/v1',
      headers: {
        'Content-Type': 'application/json'
      }
    });

    // 请求拦截器 - 添加认证令牌到每个请求
    this.api.interceptors.request.use(
      config => {
        const token = AuthService.getToken();
        if (token) {
          // 将token添加到Authorization头部
          config.headers['Authorization'] = `Bearer ${token}`;
        }
        return config;
      },
      error => {
        return Promise.reject(error);
      }
    );

    // 响应拦截器 - 处理认证失败等情况
    this.api.interceptors.response.use(
      response => response,
      error => {
        if (error.response && error.response.status === 401) {
          AuthService.logout();
          window.location.href = '/login';
        }
        return Promise.reject(error);
      }
    );
  }

  // 基本HTTP方法封装
  async get(url, params = {}) {
    try {
      const response = await this.api.get(url, { params });
      return response.data;
    } catch (error) {
      this._handleError(error);
      throw error;
    }
  }

  async post(url, data = {}) {
    try {
      const response = await this.api.post(url, data);
      return response.data;
    } catch (error) {
      this._handleError(error);
      throw error;
    }
  }

  async put(url, data = {}) {
    try {
      const response = await this.api.put(url, data);
      return response.data;
    } catch (error) {
      this._handleError(error);
      throw error;
    }
  }

  async delete(url, params = {}) {
    try {
      const response = await this.api.delete(url, { params });
      return response.data;
    } catch (error) {
      this._handleError(error);
      throw error;
    }
  }

  // 错误处理
  _handleError(error) {
    console.error('API请求错误:', error);
    if (error.response.status === 401) {
      AuthService.logout();
      window.location.href = '/login';
    }
  }
}

class ApiServices extends ApiPrefix {
  constructor() {
    super();
  }
    
  async getRobotList() {
    try {
      const data = await this.get('/robot_list');

      if ( data.code !== 0 ) { throw new Error(data.message); }

      return data;
    } catch (error) {
      throw error;
    }
  }

  async getDeviceById(id) {
    try {
      const data = await this.get(`/device_status/${id}`);
      
      if ( data.code !== 0 ) { throw new Error(data.message); }

      return data;
    } catch (error) {
      throw error;
    }
  }

  async getDeviceName(id){
    try {
      const data = await this.get(`/map-position/${id}`);

      if ( data.code !== 0 ) { throw new Error(data.message); }

      return data;
    } catch (error) {
      throw error;
    }
  }

  async getTasklist() {
    try {
      const data = await this.get(`/school-tasks/100/1`);

      if (data.code !== 0) {
        throw new Error(data.message);
      }

      return data.data;
    } catch (error) {
      throw error;
    }
  }

  async getUserInfo() {
  try {
    const user = AuthService.getUserInfo();
    const info = await this.get('/get_user_profile', { username: user.username });
    // console.log(info);
    // if (info.code !== 0) {
    //   throw new Error(info.message);
    // }
    return info;
  } catch (error) {
    throw error;
  }
}
  async getUserAvatar() {
    try {
      const userinfo = await this.getUserInfo();
      const avatar = userinfo.avatar_text;
      console.log(avatar);
      return avatar;
  } catch (error) {
    throw error;
    }
  }

  async gettargetlist() {
    try {
      const targetlist = await this.get('/target-list');
      return targetlist;
  } catch (error) {
    throw error;
    }
  }

  async updateUserProfile(data) {
      try {
        const response = await this.post('/post_user_profile', data);
        //
        // if (response.code !== 0) {
        //   throw new Error(response.message);
        // }

        return response;
      } catch (error) {
        throw error;
      }
    }

    async updateUserAvatar(data) {
      try {
        const response = await this.post('/post_user_avatar', data);
        //
        // if (response.code !== 0) {
        //   throw new Error(response.message);
        // }

        return response;
      } catch (error) {
        throw error;
      }
    }
}

export default new ApiServices();