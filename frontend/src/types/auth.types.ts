export type LoginResponse = {
  access: string;
  refresh: string;
};

export type SignupResponse = {
  id: number;
  username: string;
  password: string;
  first_name: string;
  last_name: string;
  email: string;
  date_joined: string;
  token: LoginResponse
};

export type LoginRequest = {
  username: string;
  password: string;
};

export type SignupRequest = {
  first_name: string;
  last_name: string;
  username: string;
  password: string;
  confirm_password: string;
};
