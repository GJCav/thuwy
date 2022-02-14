<template>
	<view>
		<button
			class="buttons"
			hover-class="buttons-hover"
			:style="{ '--bg-color':bgcolor , '--hover-color':hovercolor , '--duration':duration + 'ms'}"
			hover-stay-time="200"
			>
			<slot></slot>
		</button>
	</view>
</template>

<script>
	export default {
		name: "button-animation",
		data() {
			return {
				d: 1000
			};
		},
		props: {
			bgcolor: {
				type: String,
				default: "#0087A9",
				required: false
			},
			hovercolor: {
				type: String,
				default: '#00657f',
				required: false
			},
			duration: {
				type: Number,
				default: 250
			}
		}
	}
</script>

<style>
	@keyframes expand {
		0%{
			background-image: radial-gradient(circle at center, var(--hover-color) 20%,  var(--bg-color));
		}
		10% {
			background-image: radial-gradient(circle at center, var(--hover-color) 28%,  var(--bg-color));
		}

		20% {
			background-image: radial-gradient(circle at center, var(--hover-color) 36%,  var(--bg-color));
		}

		30% {
			background-image: radial-gradient(circle at center, var(--hover-color) 44%,  var(--bg-color));
		}

		40% {
			background-image: radial-gradient(circle at center, var(--hover-color) 52%,  var(--bg-color));
		}

		50% {
			background-image: radial-gradient(circle at center, var(--hover-color) 60%,  var(--bg-color));
		}

		70% {
			background-image: radial-gradient(circle at center, var(--hover-color) 76%,  var(--bg-color));
		}

		80% {
			background-image: radial-gradient(circle at center, var(--hover-color) 84%,  var(--bg-color));
		}

		90% {
			background-image: radial-gradient(circle at center, var(--hover-color) 92%,  var(--bg-color));
		}

		100% {
			background-image: radial-gradient(circle at center, var(--hover-color) 100%, var(--bg-color));
		}
	}

	.buttons {
		z-index: 100;
		width: 690rpx;
		height: 120rpx;
		border-radius: 30rpx;
		display: flex;
		align-items: center;
		justify-content: center;
		background: var(--bg-color);
	}

	.buttons-hover {
		animation: expand var(--duration) linear forwards;
	}
</style>
