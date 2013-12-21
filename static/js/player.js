// 页面对象较少
// 使用全局变量方便引用
audio = document.getElementById('audio');
btn = document.getElementById('btn');
time = document.getElementById('time');
totalProgress = document.getElementById('totalProgress');
bufferProgress = document.getElementById('bufferProgress');
currentProgress = document.getElementById('currentProgress');
change = document.getElementById('change');
duration = 0;

// 下载音乐时触发事件
// 更新缓冲条
// android手机无效
audio.addEventListener('progress', function() {
	var percent = audio.buffered.end(0) / audio.duration;
	bufferProgress.style.width = totalProgress.offsetWidth * percent + 'px';
});

// 播放时间改变事件
// 更新播放时间的文字和进度条
audio.addEventListener('timeupdate', function() {
	time.innerText = formTime(audio.currentTime) + '/' + formTime(duration);
	var percent = audio.currentTime / audio.duration;
	currentProgress.style.width = totalProgress.offsetWidth * percent + 'px';
});

// 音乐可以播放时触发此事件
// 用于音乐的自动播放
// ios手机无效
audio.addEventListener('canplay', function() {
	if (hasClass(btn, 'play')) {
		replaceClass(btn, 'play', 'pause');
		audio.play();
	}
});

// 加载音乐文件时获取到音乐时长的事件
audio.addEventListener('durationchange', function() {
	duration = Math.ceil(audio.duration);
	time.innerText = formTime(0) + '/' + formTime(duration);
});

// 音乐播放结束时触发
// 用于循环播放
audio.addEventListener('ended', function() {
	audio.play();
});

// 播放暂停事件
audio.addEventListener('pause', function() {
    if (hasClass(btn, 'pause')) {
        replaceClass(btn, 'pause', 'play');
    }
});

// 播放继续事件
audio.addEventListener('play', function() {
    if (hasClass(btn, 'play')) {
        replaceClass(btn, 'play', 'pause');
    }
});

// 播放暂停按钮点击事件
btn.addEventListener('click', function() {
	if (hasClass(btn, 'pause')) {
		replaceClass(btn, 'pause', 'play');
		audio.pause();
	} else if (hasClass(btn, 'play')) {
		replaceClass(btn, 'play', 'pause');
		audio.play();
	}
});

// 进度条点击事件
// 调整播放进度
totalProgress.addEventListener('click', function(e) {
	var leftPos = document.getElementById('controls').offsetLeft + this.offsetLeft;
	var len = e.clientX - leftPos;
	currentProgress.style.width = len + 'px';
	audio.currentTime = audio.duration * len / totalProgress.offsetWidth;
});

// 点击更换歌曲按钮刷新页面
change.addEventListener('click', function() {
	location.reload();
});

// 对DOM元素的CSS类进行操作
function hasClass(element, className) {
	return element.className.indexOf(className) >= 0;
}

function addClass(element, className) {
	if (!hasClass(element, className)) {
		element.className += className;
	}
}

function removeClass(element, className) {
	if (hasClass(element, className)) {
		var reg = new RegExp('(\\s|^)' + className + '(\\s|$)');
		element.className = element.className.replace(reg, '');
	}
}

function replaceClass(element, classNameOld, classNameNew) {
	if (hasClass(element, classNameOld)) {
		var reg = new RegExp('(\\s|^)' + classNameOld + '(\\s|$)');
		element.className = element.className.replace(reg, classNameNew);
	}
}

// 根据音乐播放的秒数得到时间字符串
function formTime(second) {
	var duration = Math.ceil(second);
	var mins = Math.floor(duration / 60);
	var secs = duration % 60;
	return '' + mins + ':' + (secs < 10 ? ('0' + secs) : secs);
}