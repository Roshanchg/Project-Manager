import { apiDelete, apiGet, apiPost } from './client';
import type {
	User,
	LoginPayload,
	CreateUserPayload,
	LoginResponse,
	RegisterResponse
} from '$lib/types';

export function me(): Promise<User> {
	return apiGet<User>('/me');
}

export function login(payload: LoginPayload): Promise<LoginResponse> {
	return apiPost<LoginResponse>('/login', payload);
}

export function register(payload: CreateUserPayload): Promise<RegisterResponse> {
	return apiPost<RegisterResponse>('/register', payload);
}

export function logout():Promise<void>{
    return apiPost<void>('/logout')
}

export function deleteMe(): Promise<{success:boolean}>{
	return apiDelete<{success:boolean}>("/deleteMe");
}