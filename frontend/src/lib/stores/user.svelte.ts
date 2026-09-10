import type { User } from '$lib/types';

let user = $state<User | null>(null);
let loading = $state(false);

export const userStore = {
	get user() {
		return user;
	},
	get loading() {
		return loading;
	},
	set(u: User | null) {
		user = u;
	},
	setLoading(v: boolean) {
		loading = v;
	},
	clear() {
		user = null;
	}
};
