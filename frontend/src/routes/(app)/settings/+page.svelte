<script lang="ts">
	import { goto } from '$app/navigation';
	import { resolve } from '$app/paths';
	import { logout } from '$lib/api/auth';
	import { deleteMe } from '$lib/api/auth';
	async function handleLogout() {
		try {
			await logout();
			await goto(resolve('/login'));
		} catch (err) {
			console.log(err);
		}
	}
	async function handleDeletion() {
		try {
			await deleteMe();
			await goto(resolve('/login'));
		} catch (err) {
			console.log(err);
		}
	}
</script>

<button onclick={handleLogout}> Logout </button>
<button onclick={handleDeletion}> Delete Me </button>
