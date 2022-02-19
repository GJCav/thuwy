<template>
	<view>
		<view class="buttons" hover-class="buttons-hover" :style="parameter" hover-stay-time="80" @click="pressButton">
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
				parameter: {
					'--bg-color': this.bgcolor,
					'--hover-color': this.hovercolor,
					'--duration': this.duration + 'ms',
					'--has-shadow': this.hasShadow
				}
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
		},
		emits: ['click'],
		methods: {
			pressButton(e) {
				this.$emit('click', e)
			}
		}
	}
</script>

<style scoped lang="scss">
	@keyframes ripple {
		0% {
			background-image: radial-gradient(circle at center, var(--hover-color) 20%, var(--bg-color));
		}

		10% {
			background-image: radial-gradient(circle at center, var(--hover-color) 28%, var(--bg-color));
		}

		20% {
			background-image: radial-gradient(circle at center, var(--hover-color) 36%, var(--bg-color));
		}

		30% {
			background-image: radial-gradient(circle at center, var(--hover-color) 44%, var(--bg-color));
		}

		40% {
			background-image: radial-gradient(circle at center, var(--hover-color) 52%, var(--bg-color));
		}

		50% {
			background-image: radial-gradient(circle at center, var(--hover-color) 60%, var(--bg-color));
		}

		70% {
			background-image: radial-gradient(circle at center, var(--hover-color) 76%, var(--bg-color));
		}

		80% {
			background-image: radial-gradient(circle at center, var(--hover-color) 84%, var(--bg-color));
		}

		90% {
			background-image: radial-gradient(circle at center, var(--hover-color) 92%, var(--bg-color));
		}

		100% {
			background-image: radial-gradient(circle at center, var(--hover-color) 100%, var(--bg-color));
		}
	}

	$duration: var(--duration);

	.buttons {
		border-radius: 30rpx;

		text-align: center;
		background: var(--bg-color);

		@if var(--has-shadow)==true {
			box-shadow: 0 3rpx 8rpx rgba(0, 0, 0, 0.3);
			/* black with 30% opacity */
		}

		transform: scale(1);
		transition: transform calc($duration/2);
		transition-timing-function: ease-in-out;
	}

	.buttons-hover {
		transform: scale(0.98);
		animation: ripple $duration linear forwards;
	}
</style>
