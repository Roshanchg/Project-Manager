<script lang="ts">
	import { goto } from '$app/navigation';
	import { resolve } from '$app/paths';
	import { login } from '$lib/api/auth';
	import { ApiError } from '$lib/api/client';

	let email = $state('');
	let password = $state('');
	let submitting = $state(false);
	let errorMessage = $state<string | null>(null);

	async function handleSubmit(e: SubmitEvent) {
		e.preventDefault();
		errorMessage = null;
		submitting = true;

		try {
			await login({ email, password });
			await goto(resolve('/dashboard'));
		} catch (err) {
			errorMessage = err instanceof ApiError ? err.message : 'Somthing went wrong. IDK ';
		} finally {
			submitting = false;
		}
	}
</script>

<main class="auth-page">
	<form class="card" onsubmit={handleSubmit}>
		<h1>Log In</h1>

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
				autocomplete="current-password"
				disabled={submitting}
			/>
		</label>

		{#if errorMessage}
			<p class="error">{errorMessage}</p>
		{/if}

		<button type="submit" disabled={submitting}>
			{submitting ? 'Logging in...' : 'Log in'}
		</button>

		<p class="hint">
			No account? <a href={resolve('/register')}>Register</a>
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

	.hint a {
		color: #0052cc;
		text-decoration: none;
	}

	.hint a:hover {
		text-decoration: underline;
	}
	@media (max-width: 480px) {
		.auth-page {
			padding: 0.75rem;
		}
		.card {
			padding: 1.25rem;
			border-radius: 8px;
		}
		h1 {
			font-size: 1.25rem;
		}
		input {
			font-size: 16px; /* ← IMPORTANT: prevents iOS auto-zoom on focus */
		}
	}
</style>
