<script lang="ts">
	import { goto } from '$app/navigation';
	import { register, login } from '$lib/api/auth';
	import { ApiError } from '$lib/api/client';
	import { resolve } from '$app/paths';

	let fullName = $state('');
	let email = $state('');
	let password = $state('');
	let confPassword = $state('');
	let submitting = $state(false);
	let errorMessage = $state<string | null>(null);
	let passwordMismatch = $derived(
		confPassword.length > 0 && password !== confPassword ? 'Passwords do not match' : null
	);

	async function handleSubmit(e: SubmitEvent) {
		e.preventDefault();
		errorMessage = null;
		if (password !== confPassword) {
			errorMessage = 'Passwords do not match';
			return;
		}
		submitting = true;

		try {
			await register({
				email,
				password,
				full_name: fullName
			});
			await login({ email, password });
			await goto(resolve('/workspace'));
		} catch (err) {
			errorMessage = err instanceof ApiError ? err.message : 'Something went wrong';
		} finally {
			submitting = false;
		}
	}
</script>

<main class="auth-page">
	<form class="card" onsubmit={handleSubmit}>
		<h1>Create an account</h1>
		<label class="field">
			<span>Full name</span>
			<input
				type="text"
				bind:value={fullName}
				required
				minlength="3"
				autocomplete="name"
				disabled={submitting}
			/>
		</label>

		<label class="field">
			<span>Email</span>
			<input type="email" bind:value={email} required autocomplete="email" disabled={submitting} />
		</label>

		<label class="field">
			<span>Password</span>
			<input
				type="password"
				bind:value={password}
				required
				minlength="8"
				autocomplete="new-password"
				disabled={submitting}
			/>
		</label>

		<label class="field">
			<span>Confirm Password</span>
			<input
				type="password"
				bind:value={confPassword}
				required
				minlength="8"
				autocomplete="new-password"
				disabled={submitting}
			/>
		</label>

		{#if errorMessage}
			<p class="error">{errorMessage}</p>
		{:else if passwordMismatch}
			<p class="error">{passwordMismatch}</p>
		{/if}

		<button type="submit" disabled={submitting}>
			{submitting ? 'Creating account...' : 'Create account'}
		</button>

		<p class="hint">
			Already have and account? <a href={resolve('/login')}>Log in</a>
		</p>
	</form>
</main>

<style>
	.auth-page {
		min-height: 100vh;
		display: grid;
		place-items: center;
		background: #f4f5f7;
		font-family: system-ui, sans-serif;
		padding: 1rem;
	}

	.card {
		width: 100%;
		max-width: 360px;
		background: white;
		padding: 2rem;
		border-radius: 10px;
		box-shadow: 0 4px 16px rgba(9, 30, 66, 0.15);
		display: flex;
		flex-direction: column;
		gap: 1rem;
	}

	h1 {
		margin: 0 0 0.5rem;
		font-size: 1.5rem;
		color: #172b4d;
		text-align: center;
	}

	.field {
		display: flex;
		flex-direction: column;
		gap: 0.25rem;
		font-size: 0.85rem;
		color: #5e6c84;
	}

	input {
		padding: 0.5rem 0.6rem;
		border: 1px solid #dfe1e6;
		border-radius: 6px;
		font-size: 0.95rem;
		font-family: inherit;
	}

	input:focus {
		outline: 2px solid #4c9aff;
		border-color: transparent;
	}

	button[type='submit'] {
		padding: 0.6rem;
		background: #0052cc;
		color: white;
		border: none;
		border-radius: 6px;
		font-size: 0.95rem;
		font-weight: 600;
		cursor: pointer;
		transition: background 0.15s;
	}

	button[type='submit']:hover:not(:disabled) {
		background: #0747a6;
	}

	button[type='submit']:disabled {
		opacity: 0.6;
		cursor: not-allowed;
	}

	.error {
		margin: 0;
		padding: 0.5rem 0.75rem;
		background: #ffebe6;
		color: #bf2600;
		border-radius: 6px;
		font-size: 0.85rem;
	}

	.hint {
		margin: 0;
		text-align: center;
		font-size: 0.85rem;
		color: #5e6c84;
	}

	.hint a {
		color: #0052cc;
		text-decoration: none;
	}

	.hint a:hover {
		text-decoration: underline;
	}
</style>
