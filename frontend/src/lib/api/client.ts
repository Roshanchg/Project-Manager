const API_PREFIX="/api/v1";

type FastApiError={detail?:string};

export class ApiError extends Error {
    status:number;
    body:unknown;
    constructor(status:number,message:string,body:unknown){
        super(message);
        this.name="ApiError";
        this.status=status;
        this.body=body;
    }

}

type RequestOptions={
    method?:"GET"|"POST" |"PUT" |"PATCH" |"DELETE";
    body?:unknown;
    headers?:Record<string,string>;

}

async function request<T>(path:string,opts:RequestOptions={}):Promise<T>{
    const {method="GET",body,headers={}}=opts;
    const init:RequestInit={
        method,
        credentials:"include",
        headers:{
            Accept:"application/json",
            ...headers,
        },
    };

    if (body!==undefined){
        init.headers={
            ...init.headers,
            'Content-Type':'application/json',
        };
        init.body=JSON.stringify(body);
    }

    const res=await fetch(`${API_PREFIX}${path}`,init);

    if (res.status===204){
        return undefined as T;
    }

    const contentType=res.headers.get("content-type")??"";
    const isJson=contentType.includes('application/json');
    const parsed=isJson?await res.json().catch(()=>null):await res.text;

    if (!res.ok){
        const detail=
        (isJson && (parsed as FastApiError)?.detail)||
        (typeof parsed==='string' && parsed ) ||
        res.statusText||
        "Request Failed";
        throw new ApiError(res.status,detail,parsed);
    }
    return parsed as T;
}

// Wrappers

export function apiGet<T>(path:string):Promise<T>{
    return request<T>(path,{method:"GET"});
}

export function apiPost<T>(path:string,body?:unknown):Promise<T>{
    return request<T>(path,{method:"POST",body});
}

export function apiPut<T>(path: string, body?: unknown): Promise<T> {
  return request<T>(path, { method: 'PUT', body });
}

export function apiPatch<T>(path: string, body?: unknown): Promise<T> {
  return request<T>(path, { method: 'PATCH', body });
}

export function apiDelete<T = void>(path: string): Promise<T> {
  return request<T>(path, { method: 'DELETE' });
}