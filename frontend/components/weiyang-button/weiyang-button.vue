<template>
	<view>
		<view
			class="buttons"
			hover-class="buttons-hover"
			:style="{ '--bg-color':bgcolor,'--hover-color':hovercolor,'--duration':duration+'ms','--has-shadow':hasShadow }"
			hover-stay-time="80"
		>
			<!-- 使用view而不是button的原因：使用button会有一个去不掉的难看的框 -->
			<slot></slot>
		</view>
	</view>
</template>

<script>
	export default {
		name: "weiyang-button",
		data() {
			return {
				
			};
		},
		props: {
			bgcolor: {
				type: String,
			},
			hovercolor: {
				type: String,
			},
			duration: {
				type: Number,
				default: 80
			},
			hasShadow: {
				type: Boolean,
				default: false
			}
		}
	}
</script>

<style scoped lang="scss">
	@keyframes ripple {
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
	
	$duration: var(--duration);
	.buttons {
		border-radius: 30rpx;
		
		outline:0 none !important; 
		border: none;
		background: var(--bg-color);
		@if var(--has-shadow)==true {
			box-shadow: 0 3rpx 8rpx rgba(0, 0, 0, 0.3); /* black with 30% opacity */
		}
		
		transform: scale(1);
		transition: transform $duration/2;
		transition-timing-function: ease-in-out;
	}

	.buttons-hover {
		transform: scale(0.99);
		animation: ripple $duration linear forwards;
	}
</style>
