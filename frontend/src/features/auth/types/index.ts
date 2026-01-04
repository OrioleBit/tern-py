export type SignupPayload = {
    name: string;
    email: string;
    password: string;
};

export type SigninPayload = {
    email: string;
    password: string;
};

export type SignupResponse = {
    id: string;
    name: string;
    email: string;
    role: string;
};

export type SigninResponse = {
    access_token: string;
    refresh_token: string;
};