<template>
  <div class="practice-view" :class="[eyeProtectionClass, `practiceMode-${practiceMode}`]">
    <div class="settings-bar">
      <div class="settings-item">
        <span>护眼模式:</span>
        <el-select v-model="eyeProtectionMode" style="width: 120px;" @change="updateEyeProtection">
          <el-option label="关闭" value="none" />
          <el-option label="暖黄" value="warm" />
          <el-option label="浅灰" value="light" />
          <el-option label="深色" value="dark" />
          <el-option label="绿底" value="green" />
        </el-select>
      </div>
      <div class="settings-item">
        <span>字体大小:</span>
        <el-button size="small" @click="decreaseFontSize">-</el-button>
        <el-select v-model="fontSize" style="width: 120px;" @change="updateFontSize">
          <el-option label="极小" :value="12" />
          <el-option label="小" :value="14" />
          <el-option label="标准" :value="16" />
          <el-option label="大" :value="18" />
          <el-option label="特大" :value="20" />
          <el-option label="超大" :value="24" />
          <el-option label="巨大" :value="28" />
          <el-option label="最大" :value="32" />
        </el-select>
        <el-button size="small" @click="increaseFontSize">+</el-button>
      </div>
      <div class="settings-item">
        <span>字体:</span>
        <el-select v-model="fontFamily" style="width: 120px;" @change="updateFontFamily">
          <el-option label="微软雅黑" value="Microsoft YaHei" />
          <el-option label="宋体" value="SimSun" />
          <el-option label="黑体" value="SimHei" />
          <el-option label="仿宋" value="FangSong" />
        </el-select>
      </div>
    </div>

    <div v-if="!practiceStarted && practiceMode !== 'memory'" class="start-screen">
      <div class="start-card">
        <h2>{{ practiceModeTitle }}</h2>
        <p>{{ practiceModeDescription }}</p>

        <div v-if="(practiceMode === 'memorize' || practiceMode === 'sequential') && practiceMode !== 'memory'" class="config-section">
          <div class="config-header">
            <h3 v-if="practiceMode === 'memorize'">📚 背题配置</h3>
            <h3 v-else>📖 顺序刷题配置</h3>
            <span class="config-tip">选择章节开始练习</span>
          </div>
          
          <div class="config-grid">
            <div class="config-card">
              <div class="config-card-header">
                <el-icon><Folder /></el-icon>
                <span>章节选择</span>
              </div>
              <div class="config-card-body">
                <div class="config-item">
                  <label>选择章节:</label>
                  <div class="chapter-select-controls">
                    <el-select v-model="config.chapterIds" multiple placeholder="选择章节" class="chapter-select">
                      <el-option v-for="ch in chapters" :key="ch.id" :label="ch.name" :value="ch.id" />
                    </el-select>
                    <div class="chapter-select-actions">
                      <el-button class="chapter-select-btn" @click="selectAllChapters" size="small">全选</el-button>
                      <el-button class="chapter-clear-btn" @click="clearAllChapters" size="small">清空</el-button>
                    </div>
                  </div>
                  <span class="config-hint">不选择则从全部题库练习</span>
                </div>
                
                <div class="config-item" v-if="practiceMode === 'sequential'">
                  <label>打乱选项:</label>
                  <div class="switch-wrapper">
                    <el-switch v-model="config.shuffleOptions" />
                    <span class="switch-label">{{ config.shuffleOptions ? '已启用' : '已禁用' }}</span>
                  </div>
                </div>
                <div v-if="practiceMode === 'memorize' || practiceMode === 'sequential'" class="config-item">
                  <label>辨析题模式:</label>
                  <div class="switch-wrapper">
                    <el-switch v-model="config.distinguishMode" />
                    <span class="switch-label">{{ config.distinguishMode ? '已开启' : '已关闭' }}</span>
                  </div>
                </div>
              </div>
            </div>
            
            <div class="config-card">
              <div class="config-card-header">
                <el-icon><Document /></el-icon>
                <span>题目预览</span>
              </div>
              <div class="config-card-body">
                <div class="preview-stat">
                  <span class="preview-label">总题数:</span>
                  <span class="preview-value">{{ selectedChapterQuestionCount }}</span>
                </div>
                <div class="preview-stat" v-if="config.chapterIds.length > 0">
                  <span class="preview-label">已选章节:</span>
                  <span class="preview-value">{{ config.chapterIds.length }}</span>
                </div>
                <div class="chapter-previews" v-if="config.chapterIds.length > 0">
                  <div v-for="chapterId in config.chapterIds" :key="chapterId" class="chapter-preview">
                    <span class="chapter-name">{{ getChapterName(chapterId) }}</span>
                    <span class="chapter-count">{{ getChapterQuestionCount(chapterId) }} 题</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div v-if="practiceMode === 'random'" class="config-section">
          <div class="config-header">
            <h3>⚙️ 抽题设置</h3>
            <span class="config-tip">配置完成后点击开始练习</span>
          </div>

          <div class="config-grid">
            <div class="config-card">
              <div class="config-card-header">
                <el-icon><Document /></el-icon>
                <span>基础设置</span>
              </div>
              <div class="config-card-body">
                <div class="config-item">
                  <label>抽题数量:</label>
                  <el-input-number v-model="config.count" :min="1" style="width: 100%;" />
                </div>

                <div class="config-item">
                  <label>每题分数:</label>
                  <el-input-number v-model="config.score" :min="1" :max="100" style="width: 100%;" />
                </div>

                <div class="config-item">
                  <label>打乱选项:</label>
                  <div class="switch-wrapper">
                    <el-switch v-model="config.shuffleOptions" />
                    <span class="switch-label">{{ config.shuffleOptions ? '已启用' : '已禁用' }}</span>
                  </div>
                </div>
              </div>
            </div>

            <div class="config-card">
              <div class="config-card-header">
                <el-icon><Folder /></el-icon>
                <span>章节范围</span>
              </div>
              <div class="config-card-body">
                <div class="config-item">
                  <label>选择章节:</label>
                  <div class="chapter-select-controls">
                    <el-select v-model="config.chapterIds" multiple placeholder="选择章节（可选）" class="chapter-select">
                      <el-option v-for="ch in chapters" :key="ch.id" :label="ch.name" :value="ch.id" />
                    </el-select>
                    <div class="chapter-select-actions">
                      <el-button class="chapter-select-btn" @click="selectAllChapters" size="small">全选</el-button>
                      <el-button class="chapter-clear-btn" @click="clearAllChapters" size="small">清空</el-button>
                    </div>
                  </div>
                  <span class="config-hint">不选择则从全部题库抽取</span>
                </div>

                <div v-if="config.chapterIds.length > 0" class="chapter-ratios-section">
                  <label class="ratios-label">各章节抽题比例:</label>
                  <div class="chapter-ratios">
                    <div v-for="chapterId in config.chapterIds" :key="chapterId" class="chapter-ratio-item">
                      <span class="chapter-ratio-label">{{ getChapterName(chapterId) }}</span>
                      <div class="ratio-input-wrapper">
                        <el-input-number
                          v-model="config.chapterRatios[chapterId]"
                          :min="0"
                          :max="100"
                          :disabled="totalChapterRatio > 100"
                          class="ratio-input"
                        />
                        <span class="ratio-unit">%</span>
                      </div>
                    </div>
                  </div>
                  <div class="ratio-summary" :class="{ 'ratio-error': totalChapterRatio > 100, 'ratio-warning': totalChapterRatio > 0 && totalChapterRatio < 100 }">
                    {{ ratioWarning }}
                  </div>
                </div>
              </div>
            </div>

            <div class="config-card">
              <div class="config-card-header">
                <el-icon><WarnTriangleFilled /></el-icon>
                <span>易错题</span>
              </div>
              <div class="config-card-body">
                <div class="config-item">
                  <label class="wrong-ratio-label">易错题比例 (%):</label>
                  <el-slider v-model="config.wrongRatio" :min="0" :max="100" show-input />
                </div>
                <div class="wrong-info-card">
                  <div class="wrong-info-title">📖 易错题说明</div>
                  <div class="wrong-info-content">
                    <ul>
                      <li>从错题本中错误次数大于2的题目中抽取</li>
                      <li>设为0则不抽取易错题</li>
                      <li>若选择了章节，易错题优先从选中章节中抽取</li>
                      <li>易错题数量不足时，自动用普通题目补足</li>
                    </ul>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div v-if="config.chapterIds.length > 0" class="preview-card">
            <div class="preview-header">
              <h4>📊 抽题预览</h4>
            </div>
            <div class="preview-content">
              <div class="preview-stat">
                <span class="preview-label">总题数:</span>
                <span class="preview-value">{{ config.count }}</span>
              </div>
              <div class="preview-stat" v-if="config.wrongRatio > 0">
                <span class="preview-label">易错题:</span>
                <span class="preview-value">约 {{ Math.ceil(config.count * config.wrongRatio / 100) }} 题</span>
              </div>
              <div class="preview-chapters" v-if="config.chapterIds.length > 0">
                <span class="preview-label">各章节:</span>
                <div class="chapter-previews">
                  <div v-for="chapterId in config.chapterIds" :key="chapterId" class="chapter-preview">
                    <span class="chapter-name">{{ getChapterName(chapterId) }}</span>
                    <span class="chapter-count">{{ typeof getChapterPreviewCount(chapterId) === 'number' ? '约 ' + getChapterPreviewCount(chapterId) + ' 题' : getChapterPreviewCount(chapterId) }}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div v-if="practiceMode === 'wrong'" class="config-section">
          <div class="config-item">
            <label>选择章节（可选）:</label>
            <el-select v-model="config.chapterIds" multiple placeholder="选择章节（不选则刷全部错题）" style="width: 100%;">
              <el-option v-for="ch in chapters" :key="ch.id" :label="ch.name" :value="ch.id" />
            </el-select>
            <p class="config-hint">错题本中共 {{ wrongCount }} 道错题</p>
          </div>
          <div class="config-item">
            <label>打乱选项:</label>
            <div class="switch-wrapper">
              <el-switch v-model="config.shuffleOptions" />
              <span class="switch-label">{{ config.shuffleOptions ? '已启用' : '已禁用' }}</span>
            </div>
          </div>
        </div>

        <div v-if="practiceMode === 'crazy'" class="config-section">
          <div class="config-header">
            <h3>⚡ 疯狂刷题配置</h3>
            <span class="config-tip">高强度练习，错误题目会重复出现</span>
          </div>
          
          <div class="config-grid">
            <div class="config-card">
              <div class="config-card-header">
                <el-icon><Folder /></el-icon>
                <span>章节选择</span>
              </div>
              <div class="config-card-body">
                <div class="config-item">
                  <label>选择章节:</label>
                  <div class="chapter-select-controls">
                    <el-select v-model="config.chapterIds" multiple placeholder="选择章节" class="chapter-select">
                      <el-option v-for="ch in chapters" :key="ch.id" :label="ch.name" :value="ch.id" />
                    </el-select>
                    <div class="chapter-select-actions">
                      <el-button class="chapter-select-btn" @click="selectAllChapters" size="small">全选</el-button>
                      <el-button class="chapter-clear-btn" @click="clearAllChapters" size="small">清空</el-button>
                    </div>
                  </div>
                  <span class="config-hint">不选择则从全部题库练习</span>
                </div>
                
                <div class="config-item">
                  <label>打乱题目顺序:</label>
                  <div class="switch-wrapper">
                    <el-switch v-model="config.shuffleQuestions" />
                    <span class="switch-label">{{ config.shuffleQuestions ? '已启用' : '已禁用' }}</span>
                  </div>
                </div>
                
                <div class="config-item">
                  <label>打乱选项顺序:</label>
                  <div class="switch-wrapper">
                    <el-switch v-model="config.shuffleOptions" />
                    <span class="switch-label">{{ config.shuffleOptions ? '已启用' : '已禁用' }}</span>
                  </div>
                </div>
              </div>
            </div>
            
            <div class="config-card">
              <div class="config-card-header">
                <el-icon><Document /></el-icon>
                <span>题目预览</span>
              </div>
              <div class="config-card-body">
                <div class="preview-stat">
                  <span class="preview-label">总题数:</span>
                  <span class="preview-value">{{ selectedChapterQuestionCount }}</span>
                </div>
                <div class="preview-stat" v-if="config.chapterIds.length > 0">
                  <span class="preview-label">已选章节:</span>
                  <span class="preview-value">{{ config.chapterIds.length }}</span>
                </div>
                <div class="chapter-previews" v-if="config.chapterIds.length > 0">
                  <div v-for="chapterId in config.chapterIds" :key="chapterId" class="chapter-preview">
                    <span class="chapter-name">{{ getChapterName(chapterId) }}</span>
                    <span class="chapter-count">{{ getChapterQuestionCount(chapterId) }} 题</span>
                  </div>
                </div>
                <div class="crazy-rules">
                  <h4>疯狂刷题规则：</h4>
                  <ul>
                    <li>✓ 正确题目直接完成，不再出现</li>
                    <li>✗ 错误题目在8题后重复出现</li>
                    <li>✗ 错误题目需答对2次才算完成</li>
                    <li>⚡ 若剩余题目不足8题，移至最后</li>
                  </ul>
                </div>
              </div>
            </div>
          </div>
        </div>

        <el-button type="primary" size="large" @click="startPractice" :disabled="practiceMode === 'sequential' && config.chapterIds.length === 0">
          开始练习
        </el-button>
      </div>
    </div>

    <div v-else class="practice-layout">
      <div class="practice-left">
        <div class="question-area">
          <div class="question-header">
            <span class="question-type">{{ currentQuestion?.question_type_name || '单选题' }}</span>
            <div class="question-actions">
              <el-button size="small" @click="toggleFavorite" :type="isFavorite ? 'warning' : 'default'">
                <el-icon><Star /></el-icon>
                {{ isFavorite ? '已收藏' : '收藏' }}
              </el-button>
              <el-button size="small" @click="toggleEditMode">
                <el-icon><Edit /></el-icon>
                {{ isEditMode ? '退出编辑' : '编辑题目' }}
              </el-button>
            </div>
            <div class="question-navigation">
              <el-button v-if="practiceMode !== 'crazy' && practiceMode !== 'memory'" size="small" @click="prevQuestion" :disabled="currentIndex === 0">上一题</el-button>
              <span class="progress">
                {{ practiceMode === 'crazy' ? `剩余 ${crazyTotalCount - crazyCompletedCount} 题` : (practiceMode === 'memory' ? `剩余 ${memoryRemainCount} 题` : `${currentIndex + 1} / ${questions.length}`) }}
              </span>
              <el-button size="small" @click="nextQuestion" :disabled="practiceMode === 'crazy' ? crazyCompletedCount >= crazyTotalCount : (practiceMode === 'memory' ? memoryCompletedCount >= memoryTotalCount : currentIndex === questions.length - 1)">下一题</el-button>
            </div>
          </div>

          <div v-if="isEditMode" class="edit-mode">
            <div class="editor-toolbar">
              <el-button size="small" @click="formatQuestion('bold')"><strong>B</strong></el-button>
              <el-button size="small" @click="formatQuestion('italic')"><em>I</em></el-button>
              <el-button size="small" @click="formatQuestion('underline')"><u>U</u></el-button>
              <el-button size="small" @click="formatQuestion('highlight-yellow')" style="background: #FFF176;">高亮</el-button>
              <el-button size="small" @click="formatQuestion('highlight-green')" style="background: #A5D6A7;">高亮</el-button>
              <el-color-picker v-model="editColor" size="small" @change="c => formatQuestion('color', c)" />
              <el-button size="small" @click="insertImageQuestion">插入图片</el-button>
              <el-button size="small" @click="insertTableQuestion">插入表格</el-button>
              <el-button size="small" @click="insertFormulaQuestion">插入公式</el-button>
              <el-button type="primary" size="small" @click="saveQuestionEdit">保存题目</el-button>
            </div>
            <div class="editor-content" ref="questionEditorRef" contenteditable></div>
          </div>

          <div v-else-if="isQuestionLoading" class="question-loading">
            <el-icon class="is-loading"><Loading /></el-icon>
            <span>加载中...</span>
          </div>
          <div v-else class="question-content" :style="contentStyle" v-html="currentQuestion?.stem_html || currentQuestion?.stem"></div>

          <div class="options-list" v-if="currentQuestion?.option_a && !isQuestionLoading">
            <div v-for="opt in displayOptions" :key="opt.label"
                 class="option-item"
                 :class="{
                   selected: isSelected(opt.label),
                   correct: (showAnswer || practiceMode === 'memorize') && isCorrectAnswer(opt.label),
                   wrong: showAnswer && isSelected(opt.label) && !isCorrectAnswer(opt.label)
                 }"
                 @click="selectOption(opt.label)">
              <span class="option-label" :style="contentStyle">{{ opt.label }}</span>
              <span class="option-text" :style="contentStyle" v-html="opt.html || opt.content"></span>
            </div>
          </div>

          <div v-if="practiceMode !== 'crazy' && practiceMode !== 'memory'" class="question-tabs">
            <div v-for="(q, idx) in questions" :key="q.id || idx"
                 class="question-tab"
                 :class="{
                   active: idx === currentIndex,
                   answered: answeredQuestions[idx] !== undefined,
                   wrong: isWrong(idx)
                 }"
                 @click="goToQuestion(idx)">
              {{ idx + 1 }}
            </div>
          </div>
        </div>
      </div>

      <div class="resize-handle" @mousedown="startResize" @touchstart.prevent="startResize"></div>

      <div class="practice-right">
        <div class="answer-section">
          <div class="answer-header">
            <h3>答案解析</h3>
            <el-button size="small" @click="toggleExplanationEdit">
              <el-icon><Edit /></el-icon>
              {{ isExplanationEdit ? '退出编辑' : '编辑解析' }}
            </el-button>
          </div>

          <div class="answer-display" v-if="showAnswer || practiceMode === 'memorize'">
            <div class="answer-result">
              <span class="answer-label">正确答案:</span>
              <span class="answer-text">{{ getDisplayAnswer() }}</span>
            </div>

            <div v-if="isExplanationEdit" class="edit-mode">
              <div class="editor-toolbar">
                <el-button size="small" @click="formatExplanation('bold')"><strong>B</strong></el-button>
                <el-button size="small" @click="formatExplanation('italic')"><em>I</em></el-button>
                <el-button size="small" @click="formatExplanation('underline')"><u>U</u></el-button>
                <el-button size="small" @click="formatExplanation('highlight-yellow')" style="background: #FFF176;">高亮</el-button>
                <el-button size="small" @click="formatExplanation('highlight-green')" style="background: #A5D6A7;">高亮</el-button>
                <el-color-picker v-model="editColor" size="small" @change="c => formatExplanation('color', c)" />
                <el-button size="small" @click="insertImageExplanation">插入图片</el-button>
                <el-button size="small" @click="insertTableExplanation">插入表格</el-button>
                <el-button size="small" @click="insertFormulaExplanation">插入公式</el-button>
                <el-button type="primary" size="small" @click="saveExplanationEdit">保存解析</el-button>
              </div>
              <div class="editor-content" ref="explanationEditorRef" contenteditable></div>
            </div>

            <div v-else class="explanation-content" :style="explanationStyle" v-html="currentQuestion?.explanation_html || currentQuestion?.explanation || '暂无解析'"></div>
          </div>

          <div v-else class="answer-hidden">
            <p>选择选项后查看答案</p>
          </div>

          <div v-if="showAnswer && practiceMode !== 'memorize'" class="action-buttons">
            <el-button v-if="config.distinguishMode && currentQuestion?.id" 
              :type="isInDistinguish(currentQuestion.id) ? 'success' : 'primary'" 
              :disabled="isInDistinguish(currentQuestion.id)" 
              @click="openDistinguishDialog">
              {{ isInDistinguish(currentQuestion.id) ? '已加入辨析题' : '加入辨析题' }}
            </el-button>
            <el-button v-if="!isInWrongBook(currentQuestion?.id)" type="warning" @click="addToWrongBook">加入错题本</el-button>
            <el-button v-else type="success" @click="removeFromWrongBook">移出错题本</el-button>
            <el-button type="primary" @click="nextQuestion" v-if="practiceMode === 'crazy' ? crazyCompletedCount < crazyTotalCount : (practiceMode === 'memory' ? memoryCompletedCount < memoryTotalCount : currentIndex < questions.length - 1)">下一题</el-button>
            <el-button @click="finishPractice">完成练习</el-button>
          </div>

          <div v-if="practiceMode === 'memorize'" class="action-buttons">
            <el-button v-if="config.distinguishMode && currentQuestion?.id" 
              :type="isInDistinguish(currentQuestion.id) ? 'success' : 'primary'" 
              :disabled="isInDistinguish(currentQuestion.id)" 
              @click="openDistinguishDialog">
              {{ isInDistinguish(currentQuestion.id) ? '已加入辨析题' : '加入辨析题' }}
            </el-button>
            <el-button @click="toggleMastered" :type="isMastered ? 'success' : 'default'">
              {{ isMastered ? '已掌握' : '标记为已掌握' }}
            </el-button>
          </div>
        </div>
      </div>
    </div>

    <!-- 图片预览模态框 -->
    <div v-if="showImagePreview" class="image-preview-overlay" @click="closeImagePreview">
      <div class="image-preview-container" @click.stop>
        <div class="image-preview-close" @click="closeImagePreview">×</div>
        <img :src="previewImageUrl" alt="预览图片" class="image-preview-img" />
      </div>
    </div>
  <!-- 辨析题弹窗 -->
  <el-dialog v-model="showDistinguishDialog" title="加入辨析题" width="75%" :close-on-click-modal="false" class="distinguish-dialog-container">
    <div v-if="distinguishQuestionData" class="distinguish-dialog">
      <div class="dialog-header">
        <div class="dialog-icon">
          <el-icon size="28"><Warning /></el-icon>
        </div>
        <div class="dialog-title-section">
          <h3>辨析题设置</h3>
          <p class="dialog-subtitle">请判断每个选项的正误，错误选项可添加正确表述</p>
        </div>
      </div>
      
      <div class="dialog-content">
        <div class="stem-card">
          <div class="stem-label">
            <el-icon><Document /></el-icon>
            <span>题干</span>
          </div>
          <div class="stem-content" v-html="distinguishQuestionData.stem_html || distinguishQuestionData.stem"></div>
        </div>

        <div class="options-section">
          <div class="options-label">
            <el-icon><List /></el-icon>
            <span>选项设置</span>
          </div>
          <div v-for="(opt, idx) in distinguishOptions" :key="idx" class="option-card" :class="{ wrong: !opt.is_correct }">
            <div class="option-header">
              <span class="option-key">{{ opt.key }}.</span>
              <span class="option-text">{{ opt.text }}</span>
              <button class="toggle-btn" :class="{ correct: opt.is_correct, wrong: !opt.is_correct }" @click="toggleOptionCorrect(idx)">
                <el-icon size="18"><Check v-if="opt.is_correct" /><Close v-else /></el-icon>
                <span>{{ opt.is_correct ? '正确' : '错误' }}</span>
              </button>
            </div>
            <div v-if="!opt.is_correct" class="corrected-input-section">
              <div class="corrected-label">
                <el-icon><EditPen /></el-icon>
                <span>正确表述</span>
              </div>
              <el-input v-model="opt.corrected_text" placeholder="请输入该选项的正确表述..." size="large" />
            </div>
          </div>
        </div>

        <div v-if="distinguishQuestionData.explanation || distinguishQuestionData.explanation_html" class="explanation-card">
          <div class="explanation-label">
            <el-icon><InfoFilled /></el-icon>
            <span>原题解析</span>
          </div>
          <div class="explanation-content" v-html="distinguishQuestionData.explanation_html || distinguishQuestionData.explanation"></div>
        </div>
      </div>
    </div>
    <template #footer>
      <div class="dialog-footer">
        <el-button @click="showDistinguishDialog = false" class="cancel-btn">取消</el-button>
        <el-button type="primary" @click="saveDistinguishQuestion" class="save-btn">保存辨析题</el-button>
      </div>
    </template>
  </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, onBeforeUnmount, watch, nextTick } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useQuizStore } from '@/store/quiz'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Loading } from '@element-plus/icons-vue'
import axios from 'axios'

const route = useRoute()
const router = useRouter()
const store = useQuizStore()

const practiceMode = computed(() => {
  const path = route.path
  if (path.includes('memory')) return 'memory'
  if (path.includes('memorize')) return 'memorize'
  if (path.includes('sequential')) return 'sequential'
  if (path.includes('random')) return 'random'
  if (path.includes('cross-chapter')) return 'cross-chapter'
  if (path.includes('wrong')) return 'wrong'
  if (path.includes('crazy')) return 'crazy'
  return 'memorize'
})

const practiceModeTitle = computed(() => {
  const titles = {
    memorize: '背题模式',
    sequential: '顺序刷题',
    random: '随机出题',
    wrong: '错题练习',
    crazy: '疯狂刷题',
    memory: '记忆刷题'
  }
  return titles[practiceMode.value] || '练习'
})

const practiceModeDescription = computed(() => {
  const descriptions = {
    memorize: '自动展示答案和解析，适合记忆背诵，可选择特定章节',
    sequential: '按章节顺序依次练习题目',
    random: '从题库中随机抽取题目进行练习',
    wrong: '针对错题本中的题目进行专项练习',
    memory: '根据刷题规划安排，执行记忆训练任务'
  }
  return descriptions[practiceMode.value] || ''
})

// 监听路由变化，重置刷题状态
watch(() => route.path, (newPath) => {
  // 重置所有状态
  practiceStarted.value = false
  questions.value = []
  currentIndex.value = 0
  selectedAnswer.value = null
  showAnswer.value = false
  answeredQuestions.value = {}
  config.count = 10
  config.chapterIds = []
  config.shuffleOptions = false
  config.distinguishMode = false
  
  // 重置疯狂刷题和记忆刷题状态
  crazyQuestionStatus.value = {}
  crazyCompletedCount.value = 0
  crazyTotalCount.value = 0
  memoryQuestionStatus.value = {}
  memoryQueue.value = []
  memoryCompletedCount.value = 0
  memoryTotalCount.value = 0
  memoryRemainCount.value = 0
})

const chapters = ref([])

const getChapterName = (chapterId) => {
  const chapter = chapters.value.find(ch => ch.id === chapterId)
  return chapter ? chapter.name : `章节${chapterId}`
}

const getChapterQuestionCount = (chapterId) => {
  const chapter = chapters.value.find(ch => ch.id === chapterId)
  return chapter?.question_count || 0
}

const questions = ref([])
const currentIndex = ref(0)
const practiceStarted = ref(false)
const showDistinguishDialog = ref(false)
const distinguishQuestionData = ref(null)
const distinguishOptions = ref([])
const isInDistinguishMap = ref({})
const showAnswer = ref(false)
const selectedAnswer = ref(null)
const lastAnswerCorrect = ref(false)
const lastCorrectAnswer = ref('')
const answeredQuestions = ref({})
const isFavorite = ref(false)
const isQuestionLoading = ref(false) // 题目加载状态，用于隐藏切换过程
const isInWrongBookMap = ref({})
const wrongCount = ref(0)
const totalQuestions = ref(0)

const selectedChapterQuestionCount = computed(() => {
  if (config.chapterIds.length === 0) {
    return totalQuestions.value
  }
  return config.chapterIds.reduce((sum, chapterId) => {
    const chapter = chapters.value.find(ch => ch.id === chapterId)
    return sum + (chapter?.question_count || 0)
  }, 0)
})

const isEditMode = ref(false)
const isExplanationEdit = ref(false)
const questionEditorRef = ref(null)
const explanationEditorRef = ref(null)
const editColor = ref('#000000')
const currentExplanationHtml = ref('')

const eyeProtectionMode = ref('none')
const fontSize = ref(16)
const fontFamily = ref('Microsoft YaHei')
const leftPanelWidth = ref(800)
const rightPanelWidth = ref(400)
const isResizing = ref(false)

// 图片预览相关
const showImagePreview = ref(false)
const previewImageUrl = ref('')

const openImagePreview = (url) => {
  previewImageUrl.value = url
  showImagePreview.value = true
}

const closeImagePreview = () => {
  showImagePreview.value = false
  previewImageUrl.value = ''
}

const startResize = (e) => {
  isResizing.value = true
  document.addEventListener('mousemove', doResize)
  document.addEventListener('mouseup', stopResize)
  document.addEventListener('touchmove', doResizeTouch, { passive: false })
  document.addEventListener('touchend', stopResize)
}

const doResize = (e) => {
  if (!isResizing.value) return
  const container = document.querySelector('.practice-layout')
  const leftPanel = document.querySelector('.practice-left')
  const rightPanel = document.querySelector('.practice-right')
  if (!container || !leftPanel || !rightPanel) return
  
  const containerRect = container.getBoundingClientRect()
  const totalWidth = containerRect.width
  const handleWidth = 16
  
  let newLeftWidth = e.clientX - containerRect.left
  
  const minLeftWidth = 280
  const minRightWidth = 200
  
  if (newLeftWidth < minLeftWidth) newLeftWidth = minLeftWidth
  if (newLeftWidth > totalWidth - handleWidth - minRightWidth) newLeftWidth = totalWidth - handleWidth - minRightWidth
  
  const leftPercentage = (newLeftWidth / totalWidth) * 100
  
  leftPanel.style.flexBasis = leftPercentage + '%'
  rightPanel.style.flexBasis = (100 - leftPercentage) + '%'
}

const doResizeTouch = (e) => {
  if (!isResizing.value) return
  e.preventDefault()
  const touch = e.touches[0]
  const container = document.querySelector('.practice-layout')
  const leftPanel = document.querySelector('.practice-left')
  const rightPanel = document.querySelector('.practice-right')
  if (!container || !leftPanel || !rightPanel) return
  
  const containerRect = container.getBoundingClientRect()
  const totalWidth = containerRect.width
  const handleWidth = 16
  
  let newLeftWidth = touch.clientX - containerRect.left
  
  const minLeftWidth = 280
  const minRightWidth = 200
  
  if (newLeftWidth < minLeftWidth) newLeftWidth = minLeftWidth
  if (newLeftWidth > totalWidth - handleWidth - minRightWidth) newLeftWidth = totalWidth - handleWidth - minRightWidth
  
  const leftPercentage = (newLeftWidth / totalWidth) * 100
  
  leftPanel.style.flexBasis = leftPercentage + '%'
  rightPanel.style.flexBasis = (100 - leftPercentage) + '%'
}

const stopResize = () => {
  isResizing.value = false
  document.removeEventListener('mousemove', doResize)
  document.removeEventListener('mouseup', stopResize)
  document.removeEventListener('touchmove', doResizeTouch)
  document.removeEventListener('touchend', stopResize)
}

const handleWindowResize = () => {
  const container = document.querySelector('.practice-layout')
  if (container) {
    const containerRect = container.getBoundingClientRect()
    const handleWidth = 8
    const totalWidth = containerRect.width
    const currentRatio = leftPanelWidth.value / (leftPanelWidth.value + rightPanelWidth.value + handleWidth)
    let newLeftWidth = totalWidth * currentRatio
    if (newLeftWidth < 300) newLeftWidth = 300
    if (newLeftWidth > totalWidth - handleWidth - 250) newLeftWidth = totalWidth - handleWidth - 250
    const newRightWidth = totalWidth - newLeftWidth - handleWidth
    leftPanelWidth.value = newLeftWidth
    rightPanelWidth.value = newRightWidth
  }
}

onBeforeUnmount(() => {
  window.removeEventListener('resize', handleWindowResize)
  // 保存当前状态
  saveCurrentState()
})

// 监听当前索引变化，自动保存
watch(currentIndex, () => {
  saveCurrentState()
})

// 监听答题情况变化，自动保存
watch(answeredQuestions, () => {
  saveCurrentState()
}, { deep: true })

const config = reactive({
  count: 10,
  score: 5,
  shuffleOptions: true,
  shuffleQuestions: false,
  distinguishMode: false,
  chapterIds: [],
  chapterRatios: {},
  wrongRatio: 20
})

// 疯狂刷题相关状态
const crazyQuestions = ref([])
const crazyCompletedCount = ref(0)
const crazyTotalCount = ref(0)
const crazyQuestionStatus = ref({}) // { questionId: { correctCount: 0, wrongCount: 0, completed: false } }

// 记忆刷题模式数据
const memoryQuestionStatus = ref({}) // { questionId: { correctAtLearning: 0, wrongCount: 0, completed: false, status: 'learning'|'reviewing' } }
const memoryQueue = ref([]) // 记忆刷题队列
const memoryCompletedCount = ref(0)
const memoryTotalCount = ref(0)
const memoryRemainCount = ref(0) // 剩余题目数量
const memoryLastAnswerCorrect = ref(null) // 记录上次答题结果（供下一题时处理反馈）

// 数组洗牌函数
const shuffleArray = (array) => {
  const newArray = [...array]
  for (let i = newArray.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1))
    ;[newArray[i], newArray[j]] = [newArray[j], newArray[i]]
  }
  return newArray
}

// 重新打乱题目选项顺序（用于记忆刷题模式题目再次出现时）
const reshuffleQuestionOptions = (question) => {
  if (!question || !question.option_a || !question.option_b) {
    return question
  }
  
  // 原始答案字母（使用保存的原始答案，如果没有则使用当前答案）
  const originalAnswerLetter = question.original_answer ? question.original_answer.toUpperCase() : (question.answer ? question.answer.toUpperCase() : '')
  
  console.log('[记忆刷题] reshuffleQuestionOptions:', {
    originalAnswerLetter,
    savedOriginalAnswer: question.original_answer,
    currentAnswer: question.answer,
    existingOriginalOptions: question.original_options
  })
  
  // 获取原始选项内容
  // 如果有保存的原始选项，使用它；否则从当前选项构建（第一次打乱时）
  const optKeys = ['option_a', 'option_b', 'option_c', 'option_d', 'option_e', 'option_f']
  let originalOptionsContent = {}
  
  if (question.original_options) {
    // 使用保存的原始选项
    originalOptionsContent = question.original_options
    console.log('[记忆刷题] 使用保存的原始选项:', originalOptionsContent)
  } else {
    // 第一次打乱，当前选项就是原始选项
    optKeys.forEach((k, i) => {
      if (question[k]) {
        originalOptionsContent[String.fromCharCode(65 + i)] = question[k] // A, B, C, D...
      }
    })
    console.log('[记忆刷题] 从当前选项构建原始选项:', originalOptionsContent)
  }
  
  // 获取原始选项值数组（按字母顺序）
  const originalOptValues = Object.entries(originalOptionsContent)
    .sort(([a], [b]) => a.localeCompare(b))
    .map(([_, val]) => val)
  
  // 打乱选项值
  const shuffled = shuffleArray([...originalOptValues])
  
  // 创建新的选项映射
  const newOptions = {}
  const letterMap = {} // 记录原始字母 -> 新字母
  shuffled.forEach((val, i) => {
    const letter = String.fromCharCode(97 + i) // a, b, c, d...
    const upperLetter = letter.toUpperCase()
    newOptions[letter] = val
    // 找出这个值在原始选项中对应的字母
    for (const [origLetter, origVal] of Object.entries(originalOptionsContent)) {
      if (origVal === val) {
        letterMap[origLetter] = upperLetter
        break
      }
    }
  })
  
  console.log('[记忆刷题] 打乱结果:', {
    originalOptValues,
    shuffled,
    letterMap,
    shuffledAnswer: letterMap[originalAnswerLetter] || question.answer
  })
  
  // 构建打乱后的题目
  return { 
    ...question,
    // 保存原始选项和原始答案，以便再次打乱时使用
    original_options: originalOptionsContent,
    original_answer: originalAnswerLetter,
    option_a: newOptions.a || null,
    option_b: newOptions.b || null,
    option_c: newOptions.c || null,
    option_d: newOptions.d || null,
    option_e: newOptions.e || null,
    option_f: newOptions.f || null,
    shuffled_options: ['A', 'B', 'C', 'D', 'E', 'F'].slice(0, shuffled.length).map((label, i) => ({
      label,
      content: shuffled[i]
    })),
    shuffled_answer: letterMap[originalAnswerLetter] || question.answer
  }
}

// 全选章节
const selectAllChapters = () => {
  config.chapterIds = chapters.value.map(ch => ch.id)
  // 只选中章节，不设置比例，让用户自己决定是否设置
}

// 清空章节选择
const clearAllChapters = () => {
  config.chapterIds = []
  config.chapterRatios = {}
}

// 检查章节比例总和
const totalChapterRatio = computed(() => {
  return config.chapterIds.reduce((sum, id) => {
    return sum + (config.chapterRatios[id] || 0)
  }, 0)
})

// 判断是否设置了章节比例
const hasChapterRatios = computed(() => {
  return config.chapterIds.some(id => (config.chapterRatios[id] || 0) > 0)
})

// 计算最终各章节比例
const finalChapterRatios = computed(() => {
  const ratios = {}
  if (!config.chapterIds.length) return ratios
  
  if (hasChapterRatios.value) {
    const setChapters = config.chapterIds.filter(id => (config.chapterRatios[id] || 0) > 0)
    const unsetChapters = config.chapterIds.filter(id => (config.chapterRatios[id] || 0) === 0)
    
    // 先设置已配置的比例
    setChapters.forEach(id => {
      ratios[id] = config.chapterRatios[id] || 0
    })
    
    // 分配剩余比例给未设置的章节
    if (unsetChapters.length > 0) {
      const remaining = 100 - Object.values(ratios).reduce((a, b) => a + b, 0)
      if (remaining > 0) {
        const eachRatio = Math.floor(remaining / unsetChapters.length)
        unsetChapters.forEach((id, i) => {
          if (i === unsetChapters.length - 1) {
            ratios[id] = remaining - eachRatio * (unsetChapters.length - 1)
          } else {
            ratios[id] = eachRatio
          }
        })
      }
    }
  }
  
  return ratios
})

// 比例警告
const ratioWarning = computed(() => {
  const total = totalChapterRatio.value
  if (!hasChapterRatios.value) return '未设置章节比例，将从选中章节随机抽取'
  if (total > 100) return `比例总和超过100% (${total}%)，请调整`
  if (total < 100) return `剩余 ${100 - total}% 将分配给未设置比例的章节`
  return '比例总和100%，完全按章节比例抽取'
})

// 计算各章节抽题数量预览
const getChapterPreviewCount = (chapterId) => {
  if (!hasChapterRatios.value) {
    return '随机'
  }
  const ratio = finalChapterRatios.value[chapterId] || 0
  return Math.ceil(config.count * ratio / 100)
}

// 保存当前刷题状态
const saveCurrentState = () => {
  // 记忆刷题模式不保存状态
  if (practiceMode.value === 'memory') {
    return
  }
  
  if (practiceStarted.value) {
    store.savePracticeSession(practiceMode.value, {
      questions: questions.value,
      currentIndex: currentIndex.value,
      practiceStarted: practiceStarted.value,
      showAnswer: showAnswer.value,
      answeredQuestions: answeredQuestions.value,
      config: { ...config }
    })
  }
}

// 恢复保存的刷题状态
const restoreSavedState = async () => {
  // 记忆刷题模式不恢复保存状态，每次重新加载任务
  if (practiceMode.value === 'memory') {
    return false
  }
  
  const saved = store.getSavedPracticeSession(practiceMode.value)
  if (saved && saved.practiceStarted) {
    try {
      const { value } = await ElMessageBox.confirm(
        '检测到您有未完成的刷题进程，是否继续？',
        '提示',
        {
          confirmButtonText: '继续',
          cancelButtonText: '重新开始',
          type: 'info'
        }
      )
      if (value) {
        // 恢复状态
        questions.value = saved.questions
        currentIndex.value = saved.currentIndex
        practiceStarted.value = saved.practiceStarted
        showAnswer.value = saved.showAnswer
        answeredQuestions.value = saved.answeredQuestions
        config.count = saved.config?.count || 10
        config.chapterIds = saved.config?.chapterIds || []
        return true
      } else {
        // 清除保存的状态
        store.clearSavedPracticeSession(practiceMode.value)
      }
    } catch (error) {
      // 用户点击取消或关闭
      store.clearSavedPracticeSession(practiceMode.value)
    }
  }
  return false
}

const eyeProtectionClass = computed(() => {
  if (eyeProtectionMode.value === 'none') return ''
  return `eye-protection-${eyeProtectionMode.value}`
})

const contentStyle = computed(() => ({
  fontSize: fontSize.value + 'px !important',
  fontFamily: fontFamily.value + ' !important'
}))

// 解析内容的字体大小，最多只到24px
const explanationStyle = computed(() => ({
  fontSize: Math.min(fontSize.value, 24) + 'px !important',
  fontFamily: fontFamily.value + ' !important'
}))

const currentQuestion = computed(() => {
  return questions.value[currentIndex.value] || null
})

const displayOptions = computed(() => {
  if (!currentQuestion.value) return []
  if (currentQuestion.value.shuffled_options) {
    return currentQuestion.value.shuffled_options
  }
  const optionKeys = ['option_a', 'option_b', 'option_c', 'option_d', 'option_e', 'option_f']
  const labels = ['A', 'B', 'C', 'D', 'E', 'F']
  return optionKeys.map((key, i) => {
    const q = currentQuestion.value
    return {
      label: labels[i],
      content: q[key],
      html: q[`${key}_html`]
    }
  }).filter(opt => opt.content)
})

const getDisplayAnswer = () => {
  if (!currentQuestion.value) return ''
  // 记忆刷题模式：始终使用打乱后的正确答案（如果有），否则使用原始答案
  if (practiceMode.value === 'memory') {
    // 如果有打乱后的答案，使用它
    if (currentQuestion.value?.shuffled_answer) {
      return currentQuestion.value.shuffled_answer
    }
    // 否则使用原始答案（初学题目不打乱选项）
    return currentQuestion.value?.answer || ''
  }
  // 其他模式：优先使用后端返回的答案
  if (lastCorrectAnswer.value) return lastCorrectAnswer.value
  // 考虑打乱选项的情况：如果选项被打乱，显示打乱后的正确答案
  if (currentQuestion.value?.shuffled_options && currentQuestion.value?.shuffled_answer) {
    return currentQuestion.value.shuffled_answer
  }
  return currentQuestion.value?.answer || ''
}

const isSelected = (label) => {
  return answeredQuestions.value[currentIndex.value] === label
}

const isCorrectAnswer = (label) => {
  const q = currentQuestion.value
  const answer = q?.shuffled_options ? (q?.shuffled_answer || '') : (q?.answer || '')
  return answer.toUpperCase().includes(label.toUpperCase())
}

const isWrong = (idx) => {
  if (answeredQuestions.value[idx] === undefined) return false
  const q = questions.value[idx]
  const answer = answeredQuestions.value[idx]
  const correctAnswer = q?.shuffled_options ? (q?.shuffled_answer || '') : (q?.answer || '')
  return !correctAnswer.toUpperCase().includes(answer?.toUpperCase())
}

const isMastered = computed(() => {
  return false
})

const selectOption = async (label) => {
  if (practiceMode.value === 'memorize' || showAnswer.value) return
  if (!currentQuestion.value) return

  answeredQuestions.value[currentIndex.value] = label
  showAnswer.value = true

  // 记忆刷题模式下使用 question_id，普通模式使用 id
  const questionId = currentQuestion.value.question_id || currentQuestion.value.id
  const expectedAnswer = currentQuestion.value?.shuffled_options ? currentQuestion.value?.shuffled_answer : null
  
  console.log('[记忆刷题] selectOption:', {
    label,
    expectedAnswer,
    questionId,
    shuffled_options: currentQuestion.value?.shuffled_options,
    shuffled_answer: currentQuestion.value?.shuffled_answer,
    answer: currentQuestion.value?.answer
  })
  
  try {
    const result = await store.submitAnswer(questionId, label, expectedAnswer)
    console.log('[记忆刷题] submitAnswer result:', result)
    lastAnswerCorrect.value = result.is_correct
    lastCorrectAnswer.value = result.correct_answer || ''

    if (!result.is_correct) {
      isInWrongBookMap.value[questionId] = true
    }

    // 疯狂刷题模式特殊处理
    if (practiceMode.value === 'crazy') {
      const status = crazyQuestionStatus.value[questionId]
      
      if (result.is_correct) {
        // 第一次就答对，直接完成
        if (status.wrongCount === 0 && !status.completed) {
          status.completed = true
          crazyCompletedCount.value++
        }
        // 之前答错了，正在验证阶段
        else if (status.wrongCount > 0 && !status.completed) {
          status.correctCount++
          // 验证答对两次，完成
          if (status.correctCount >= 2) {
            status.completed = true
            crazyCompletedCount.value++
          }
          // 验证答对一次，在12题后再次验证
          else if (status.correctCount === 1) {
            const insertIndex = Math.min(currentIndex.value + 12, questions.value.length)
            const currentQuestion = questions.value[currentIndex.value]
            questions.value.splice(insertIndex, 0, currentQuestion)
          }
        }
      } else {
        // 答错
        status.wrongCount++
        // 重置验证计数
        status.correctCount = 0
        // 在8题后重新插入该题
        const insertIndex = Math.min(currentIndex.value + 8, questions.value.length)
        const currentQuestion = questions.value[currentIndex.value]
        questions.value.splice(insertIndex, 0, currentQuestion)
      }
    }
    
    // 记忆刷题模式：只记录答案结果，不立即处理反馈（等点击下一题时处理）
    if (practiceMode.value === 'memory') {
      // 记录当前题目的答题结果，供下一题时使用
      memoryLastAnswerCorrect.value = result.is_correct
    }
  } catch (error) {
    console.error('Submit answer failed:', error)
  }
}

// 记忆刷题提交反馈到后端
const submitMemoryFeedback = async (recordId, feedback) => {
  if (!recordId) return null
  try {
    const response = await axios.post('/api/practice-plan/feedback?user_id=default_user', {
      record_id: recordId,
      feedback: feedback
    })
    // 返回后端响应，以便更新进度
    return response.data
  } catch (error) {
    console.error('Submit memory feedback failed:', error)
    return null
  }
}

const prevQuestion = () => {
  if (currentIndex.value > 0) {
    currentIndex.value--
    resetQuestionState()
  }
}

const nextQuestion = async () => {
  // 记忆刷题模式：先处理当前题目的反馈，再切换到下一题
  if (practiceMode.value === 'memory') {
    // 立即隐藏题目内容，防止用户看到切换过程
    isQuestionLoading.value = true
    showAnswer.value = false
    
    // 等待 Vue 更新完成，确保题目内容已隐藏
    await nextTick()
    
    // 处理当前题目的反馈
    if (memoryLastAnswerCorrect.value !== null) {
      const currentIdx = currentIndex.value
      const currentQ = questions.value[currentIdx]
      const actualQuestionId = currentQ.question_id
      const status = memoryQuestionStatus.value[actualQuestionId]
      
      console.log('[记忆刷题] 处理反馈:', {
        currentIdx,
        actualQuestionId,
        isCorrect: memoryLastAnswerCorrect.value,
        statusBefore: status ? { ...status } : null,
        questionCountBefore: questions.value.length
      })
      
      if (status) {
        console.log('[记忆刷题] 当前状态:', {
          record_id: status.record_id,
          correctAtLearning: status.correctAtLearning,
          status: status.status,
          completed: status.completed
        })
        
        // 保存题目副本（用于重新插入）
        const questionCopy = { ...currentQ }
        
        // 从数组中移除当前题目
        questions.value.splice(currentIdx, 1)
        
        if (memoryLastAnswerCorrect.value) {
          // 答对
          const response = await submitMemoryFeedback(status.record_id, 'correct')
          
          console.log('[记忆刷题] submitMemoryFeedback 返回:', JSON.stringify(response))
          // submitMemoryFeedback 返回 response.data，即 {status: 'ok', data: record.to_dict(), remaining: N}
          // record.to_dict() 直接在 response.data 中
          if (response && response.data) {
            const recordData = response.data
            if (recordData.correct_at_learning_count !== undefined) {
              status.correctAtLearning = recordData.correct_at_learning_count
            }
            if (recordData.completed !== undefined) {
              status.completed = recordData.completed
            }
            if (recordData.status) {
              status.status = recordData.status
            }
            console.log('[记忆刷题] 后端返回数据:', recordData)
          } else {
            console.log('[记忆刷题] 无法读取后端数据: response=', response ? 'exists' : 'null')
          }
          
          // 防御性修复：如果 correctAtLearning >= 2，强制设置完成状态
          // 解决后端返回的 completed 值可能被覆盖的问题
          if (status.correctAtLearning >= 2) {
            status.completed = true
            status.status = 'reviewing'
            console.log('[记忆刷题] 强制设置完成状态: correctAtLearning =', status.correctAtLearning)
          }
          
          if (status.status === 'learning') {
            // 初学状态：检查是否需要重新插入
            if (!status.completed) {
              // 还未完成，需要重新插入
              const insertIndex = Math.min(currentIdx + 12, questions.value.length)
              console.log('[记忆刷题] 插入前 questionCopy 选项:', {
                original_options: questionCopy.original_options,
                original_answer: questionCopy.original_answer,
                currentOptions: {
                  A: questionCopy.option_a,
                  B: questionCopy.option_b,
                  C: questionCopy.option_c,
                  D: questionCopy.option_d
                }
              })
              const reshuffledQ = reshuffleQuestionOptions(questionCopy)
              console.log('[记忆刷题] 插入后 reshuffledQ 选项:', {
                shuffled_options: reshuffledQ.shuffled_options,
                shuffled_answer: reshuffledQ.shuffled_answer,
                newOptions: {
                  A: reshuffledQ.option_a,
                  B: reshuffledQ.option_b,
                  C: reshuffledQ.option_c,
                  D: reshuffledQ.option_d
                }
              })
              questions.value.splice(insertIndex, 0, reshuffledQ)
              console.log('[记忆刷题] 初学答对，插入到索引', insertIndex, 'correctAtLearning=', status.correctAtLearning)
            } else {
              // 完成，移出任务列表
              console.log('[记忆刷题] 初学阶段完成，移出列表')
              memoryCompletedCount.value++
              memoryRemainCount.value--
            }
          } else {
            // 复习中状态：做对一次完成当日任务
            console.log('[记忆刷题] 复习中答对，完成当日任务，移出列表')
            memoryCompletedCount.value++
            memoryRemainCount.value--
          }
        } else {
          // 答错
          const response = await submitMemoryFeedback(status.record_id, 'wrong')
          
          console.log('[记忆刷题] 答错 submitMemoryFeedback 返回:', JSON.stringify(response))
          // 使用后端返回的状态更新前端
          if (response && response.data) {
            const recordData = response.data
            if (recordData.correct_at_learning_count !== undefined) {
              status.correctAtLearning = recordData.correct_at_learning_count
            }
            if (recordData.status) {
              status.status = recordData.status
            }
            if (recordData.completed !== undefined) {
              status.completed = recordData.completed
            }
            console.log('[记忆刷题] 答错后端返回数据:', recordData)
          }
          
          // 答错总是需要重新插入（安排在8题后）
          const insertIndex = Math.min(currentIdx + 8, questions.value.length)
          const reshuffledQ = reshuffleQuestionOptions(questionCopy)
          questions.value.splice(insertIndex, 0, reshuffledQ)
          console.log('[记忆刷题] 答错，插入到索引', insertIndex)
        }
      }
      memoryLastAnswerCorrect.value = null
    }
    
    // 检查是否所有题目都已完成
    if (memoryCompletedCount.value >= memoryTotalCount.value) {
      isQuestionLoading.value = false
      ElMessage.success('🎉 恭喜！所有题目已完成！')
      return
    }
    if (questions.value.length === 0) {
      isQuestionLoading.value = false
      ElMessage.success('🎉 恭喜！所有题目已完成！')
      return
    }
    
    // 从头开始找到第一个未完成的题目
    let foundIdx = -1
    for (let i = 0; i < questions.value.length; i++) {
      const q = questions.value[i]
      const questionId = q?.question_id
      if (!questionId || !memoryQuestionStatus.value[questionId]?.completed) {
        foundIdx = i
        break
      }
    }
    
    if (foundIdx !== -1) {
      currentIndex.value = foundIdx
      await nextTick()
      isQuestionLoading.value = false
      resetQuestionState()
      return
    }
    
    // 所有题目都已完成
    isQuestionLoading.value = false
    if (memoryCompletedCount.value < memoryTotalCount.value) {
      ElMessage.info('还有题目未完成，请继续答题')
    } else {
      ElMessage.success('🎉 恭喜！所有题目已完成！')
    }
    return
  }
  
  // 疯狂刷题模式：检查是否所有题目都已完成
  if (practiceMode.value === 'crazy') {
    if (crazyCompletedCount.value >= crazyTotalCount.value) {
      ElMessage.success('🎉 恭喜！所有题目已完成！')
      return
    }
    if (questions.value.length === 0) {
      ElMessage.success('🎉 恭喜！所有题目已完成！')
      return
    }
    
    // 跳过已完成的题目，找到下一个未完成的题目
    let nextIdx = currentIndex.value + 1
    while (nextIdx < questions.value.length) {
      const qId = questions.value[nextIdx]?.id
      if (!qId || !crazyQuestionStatus.value[qId]?.completed) {
        currentIndex.value = nextIdx
        resetQuestionState()
        return
      }
      nextIdx++
    }
    
    // 到达末尾，检查是否还有未完成的题目
    if (crazyCompletedCount.value < crazyTotalCount.value) {
      ElMessage.info('还有题目未完成，请继续答题')
    } else {
      ElMessage.success('🎉 恭喜！所有题目已完成！')
    }
    return
  }
  
  // 记忆刷题模式：检查是否所有题目都已完成
  if (practiceMode.value === 'memory') {
    if (memoryCompletedCount.value >= memoryTotalCount.value) {
      ElMessage.success('🎉 恭喜！所有题目已完成！')
      return
    }
    if (questions.value.length === 0) {
      ElMessage.success('🎉 恭喜！所有题目已完成！')
      return
    }
    
    // 跳过已完成的题目，找到下一个未完成的题目
    let nextIdx = currentIndex.value + 1
    while (nextIdx < questions.value.length) {
      const q = questions.value[nextIdx]
      const questionId = q?.question_id
      if (!questionId || !memoryQuestionStatus.value[questionId]?.completed) {
        currentIndex.value = nextIdx
        resetQuestionState()
        return
      }
      nextIdx++
    }
    
    // 到达末尾，从开头重新检查是否有未完成的题目
    nextIdx = 0
    while (nextIdx < questions.value.length) {
      const q = questions.value[nextIdx]
      const questionId = q?.question_id
      if (!questionId || !memoryQuestionStatus.value[questionId]?.completed) {
        currentIndex.value = nextIdx
        resetQuestionState()
        return
      }
      nextIdx++
    }
    
    // 所有题目都已完成
    if (memoryCompletedCount.value < memoryTotalCount.value) {
      ElMessage.info('还有题目未完成，请继续答题')
    } else {
      ElMessage.success('🎉 恭喜！所有题目已完成！')
    }
    return
  }
  
  if (currentIndex.value < questions.value.length - 1) {
    currentIndex.value++
    resetQuestionState()
  } else if (practiceMode.value === 'crazy') {
    // 疯狂刷题模式：到达最后一题时检查是否还有未完成的题目
    if (crazyCompletedCount.value < crazyTotalCount.value) {
      ElMessage.info('还有题目未完成，请继续答题')
    } else {
      ElMessage.success('🎉 恭喜！所有题目已完成！')
    }
  } else if (practiceMode.value === 'memory') {
    // 记忆刷题模式：检查是否还有未完成的题目
    if (memoryCompletedCount.value < memoryTotalCount.value) {
      ElMessage.info('还有题目未完成，请继续答题')
    } else {
      ElMessage.success('🎉 恭喜！所有题目已完成！')
    }
  }
}

const goToQuestion = (index) => {
  currentIndex.value = index
  resetQuestionState()
}

const resetQuestionState = () => {
  // 记忆刷题模式：每次切换题目都隐藏答案，让用户重新作答
  if (practiceMode.value === 'memory') {
    showAnswer.value = false
    lastCorrectAnswer.value = ''
    checkFavorite()
    return
  }
  showAnswer.value = answeredQuestions.value[currentIndex.value] !== undefined
  lastCorrectAnswer.value = ''
  checkFavorite()
  if (config.distinguishMode && questions.value[currentIndex.value]?.id) {
    checkDistinguishStatus(questions.value[currentIndex.value].id)
  }
}

const startPractice = async () => {
  if (practiceStarted.value && questions.value.length > 0) {
    return
  }
  
  try {
    // 先尝试恢复保存的状态
    const restored = await restoreSavedState()
    if (restored) {
      totalQuestions.value = questions.value.length
      await checkFavorite()
      return
    }

    let result
    if (practiceMode.value === 'memorize') {
      const params = { per_page: 10000 }
      if (config.chapterIds.length > 0) {
        // 支持多章节选择
        params.chapter_ids = config.chapterIds
      }
      result = await store.practiceMemorize(params)
      questions.value = result.data
    } else if (practiceMode.value === 'sequential') {
      result = await store.practiceSequential({
        chapter_ids: config.chapterIds,
        shuffle_options: config.shuffleOptions
      })
      questions.value = result.data
    } else if (practiceMode.value === 'random') {
      result = await store.practiceRandom({
        count: config.count,
        score: config.score,
        shuffle_options: config.shuffleOptions,
        chapter_ids: config.chapterIds,
        chapter_ratios: config.chapterRatios,
        wrong_ratio: config.wrongRatio
      })
      questions.value = result.data
    } else if (practiceMode.value === 'wrong') {
      const modeParam = route.query.mode
      const sessionIdParam = route.query.sessionId
      const chaptersParam = route.query.chapters
      const shuffleOptionsParam = route.query.shuffle_options
      const useShuffleOptions = shuffleOptionsParam === 'true' ? true : (shuffleOptionsParam === 'false' ? false : config.shuffleOptions)

      if (modeParam === 'wrong_selected' && sessionIdParam) {
        console.log('DEBUG: Loading pre-selected wrong questions with session:', sessionIdParam)
        const wrongIds = route.query.wrongIds ? JSON.parse(route.query.wrongIds) : []
        if (wrongIds.length > 0) {
          const res = await axios.post('/api/wrong-questions/practice', {
            user_id: store.userId,
            shuffle: false,
            wrong_ids: wrongIds
          })
          questions.value = res.data.data || []
        } else {
          questions.value = store.questions || []
        }
        totalQuestions.value = questions.value.length
        practiceStarted.value = true
        showAnswer.value = false
        await checkFavorite()
        return
      } else {
        let apiParams = {
          user_id: store.userId,
          shuffle: true,
          shuffle_options: useShuffleOptions
        }

        if (chaptersParam) {
          const chapterIds = chaptersParam.split(',').map(id => parseInt(id))
          console.log('DEBUG: Using route chapter selection:', chapterIds)
          apiParams.chapter_ids = chapterIds
        } else if (config.chapterIds.length > 0) {
          const chapterIds = config.chapterIds.map(id => parseInt(id))
          console.log('DEBUG: Using config chapter selection:', chapterIds)
          apiParams.chapter_ids = chapterIds
        } else {
          console.log('DEBUG: Loading all wrong questions')
        }

        console.log('DEBUG: API params:', apiParams)
        result = await fetch('/api/wrong-questions/practice', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(apiParams)
        }).then(res => res.json())

        console.log('DEBUG: Practice result:', result)
        questions.value = result.data || []
      }
    } else if (practiceMode.value === 'crazy') {
      // 疯狂刷题模式
      const params = { per_page: 10000 }
      if (config.chapterIds.length > 0) {
        params.chapter_ids = config.chapterIds
      }
      result = await store.practiceMemorize(params)
      questions.value = result.data
      
      // 打乱题目顺序（如果配置了）
      if (config.shuffleQuestions) {
        questions.value = shuffleArray(questions.value)
      }
      
      // 初始化疯狂刷题状态
      crazyQuestionStatus.value = {}
      questions.value.forEach(q => {
        crazyQuestionStatus.value[q.id] = {
          correctCount: 0,
          wrongCount: 0,
          completed: false
        }
      })
      crazyTotalCount.value = questions.value.length
      crazyCompletedCount.value = 0
    } else if (practiceMode.value === 'memory') {
      // 记忆刷题模式：从刷题规划获取任务
      try {
        const response = await axios.get('/api/practice-plan/tasks', {
          params: {
            user_id: store.userId
          }
        })
        
        if (response.data.status === 'ok') {
          const tasks = response.data.data || []
          
          if (tasks.length === 0) {
            ElMessage.warning('暂无刷题任务，请在刷题规划中添加题目')
            return
          }
          
          // 初始化记忆刷题队列
          memoryQuestionStatus.value = {}
          memoryQueue.value = []
          
          // 分离初学中和复习中的题目
          const learningTasks = tasks.filter(t => t.status === 'learning')
          const reviewingTasks = tasks.filter(t => t.status === 'reviewing')
          
          // 初学中题目：按加入顺序，不打乱
          // 根据 learning_repetition 安排题目位置
          // 先处理 learning_repetition = 0 的题目（立即出现）
          // 再处理 learning_repetition > 0 的题目（安排在指定位置）
          const immediateTasks = learningTasks.filter(t => t.learning_repetition === 0)
          const delayedTasks = learningTasks.filter(t => t.learning_repetition > 0)
          
          // 立即出现的题目
          immediateTasks.forEach(t => {
            const isCompleted = t.correct_at_learning_count >= 2
            memoryQuestionStatus.value[t.question_id] = {
              correctAtLearning: t.correct_at_learning_count || 0,
              wrongCount: 0,
              completed: isCompleted,
              status: isCompleted ? 'completed' : 'learning',
              record_id: t.id,
              waitingForRepeat: 0,
              needVerify: t.correct_at_learning_count >= 1,
              verified: isCompleted
            }
            // 只有未完成的题目才加入队列
            if (!isCompleted) {
              memoryQueue.value.push(t.question_id)
            }
          })
          
          // 延迟出现的题目（安排在指定位置）
          delayedTasks.forEach(t => {
            const isCompleted = t.correct_at_learning_count >= 2
            memoryQuestionStatus.value[t.question_id] = {
              correctAtLearning: t.correct_at_learning_count || 0,
              wrongCount: 0,
              completed: isCompleted,
              status: isCompleted ? 'completed' : 'learning',
              record_id: t.id,
              waitingForRepeat: t.learning_repetition,
              needVerify: t.correct_at_learning_count >= 1,
              verified: isCompleted
            }
            // 只有未完成的题目才加入队列
            if (!isCompleted) {
              // 安排在队列的指定位置（末尾）
              memoryQueue.value.push(t.question_id)
            }
          })
          
          // 复习中题目：打乱顺序
          const shuffledReviewing = shuffleArray([...reviewingTasks])
          shuffledReviewing.forEach(t => {
            memoryQuestionStatus.value[t.question_id] = {
              correctAtLearning: 0,
              wrongCount: 0,
              completed: false,
              status: 'reviewing',
              record_id: t.id
            }
            memoryQueue.value.push(t.question_id)
          })
          
          // 后端返回的to_dict已经是扁平化数据，题目字段直接在同一层级
          // 构建questionId到task的映射
          const questionMap = {}
          tasks.forEach(t => {
            questionMap[t.question_id] = t
          })
          
          // 按队列顺序重新排列
          questions.value = memoryQueue.value.map(qid => questionMap[qid]).filter(q => q)
          
          // 计算已完成和剩余题目数量
          let initialCompleted = 0
          let initialRemaining = 0
          memoryQueue.value.forEach(qid => {
            const status = memoryQuestionStatus.value[qid]
            if (status) {
              if (status.completed) {
                initialCompleted++
              } else {
                initialRemaining++
              }
            }
          })
          memoryTotalCount.value = initialCompleted + initialRemaining
          memoryCompletedCount.value = initialCompleted
          memoryRemainCount.value = initialRemaining
          
          // 打乱复习题目的选项（初学题目不打乱选项）
          questions.value.forEach((q, idx) => {
            if (memoryQuestionStatus.value[q.question_id]?.status === 'reviewing') {
              // 复习题目：打乱选项
              if (q.option_a && q.option_b) {
                // 获取原始选项和答案的对应关系
                const originalAnswer = q.answer.toUpperCase()
                const optKeys = ['option_a', 'option_b', 'option_c', 'option_d', 'option_e', 'option_f']
                const originalOptions = {}
                optKeys.forEach((k, i) => {
                  if (q[k]) {
                    originalOptions[String.fromCharCode(65 + i)] = q[k] // A, B, C, D...
                  }
                })
                
                // 获取选项值数组
                const optValues = optKeys.map(k => q[k]).filter(v => v)
                // 打乱选项值
                const shuffled = shuffleArray([...optValues])
                
                // 创建新的选项映射
                const newOptions = {}
                const letterMap = {} // 记录哪个位置对应哪个字母
                shuffled.forEach((val, i) => {
                  const letter = String.fromCharCode(97 + i) // a, b, c, d...
                  const upperLetter = letter.toUpperCase()
                  newOptions[letter] = val
                  // 找出这个值原来对应的字母
                  for (const [origLetter, origVal] of Object.entries(originalOptions)) {
                    if (origVal === val) {
                      letterMap[origLetter] = upperLetter
                      break
                    }
                  }
                })
                
                // 构建打乱后的题目
                const shuffledQuestion = { 
                  ...q,
                  // 保存原始选项和原始答案，以便再次打乱时使用
                  original_options: originalOptions,
                  original_answer: originalAnswer,
                  option_a: newOptions.a || null,
                  option_b: newOptions.b || null,
                  option_c: newOptions.c || null,
                  option_d: newOptions.d || null,
                  option_e: newOptions.e || null,
                  option_f: newOptions.f || null,
                  shuffled_options: ['A', 'B', 'C', 'D', 'E', 'F'].slice(0, shuffled.length).map((label, i) => ({
                    label,
                    content: shuffled[i]
                  })),
                  shuffled_answer: letterMap[originalAnswer] || q.answer
                }
                questions.value[idx] = shuffledQuestion
              }
            }
          })
          
          ElMessage.success(`已加载 ${questions.value.length} 道刷题任务`)
        } else {
          ElMessage.warning('获取刷题任务失败')
          return
        }
      } catch (error) {
        console.error('ERROR: Failed to load practice plan tasks:', error)
        ElMessage.error('加载刷题任务失败')
        return
      }
    }

    practiceStarted.value = true
    if (practiceMode.value === 'memory') {
      totalQuestions.value = memoryTotalCount.value
    } else {
      totalQuestions.value = result.total || questions.value.length
    }
    showAnswer.value = practiceMode.value === 'memorize'
    await checkFavorite()
    if (config.distinguishMode && questions.value.length > 0) {
      await checkDistinguishStatus(questions.value[0].id)
    }
  } catch (error) {
    console.error('ERROR: Failed to start practice:', error)
    if (error.response) {
      console.error('ERROR: Response data:', error.response.data)
      console.error('ERROR: Response status:', error.response.status)
    } else if (error.request) {
      console.error('ERROR: No response received:', error.request)
    } else {
      console.error('ERROR: Request setup error:', error.message)
    }
    ElMessage.error('加载题目失败')
  }
}

const checkFavorite = async () => {
  if (!currentQuestion.value?.id) return
  try {
    isFavorite.value = await store.checkFavorite(currentQuestion.value.id)
  } catch (error) {
    isFavorite.value = false
  }
}

const toggleFavorite = async () => {
  if (!currentQuestion.value?.id) return
  try {
    if (isFavorite.value) {
      await store.removeFromFavorites(currentQuestion.value.id)
      isFavorite.value = false
      ElMessage.success('已取消收藏')
    } else {
      await store.addToFavorites(currentQuestion.value.id)
      isFavorite.value = true
      ElMessage.success('已添加收藏')
    }
  } catch (error) {
    ElMessage.error('操作失败')
  }
}

const isInWrongBook = (questionId) => {
  return isInWrongBookMap.value[questionId] || false
}

const isInDistinguish = (questionId) => {
  return isInDistinguishMap.value[questionId] || false
}

const checkDistinguishStatus = async (questionId) => {
  if (!questionId) return false
  try {
    const res = await axios.get(`/api/distinguish/check/${questionId}`)
    isInDistinguishMap.value[questionId] = res.data.exists || false
    return res.data.exists
  } catch (e) {
    console.error(e)
    return false
  }
}

const addToWrongBook = async () => {
  if (!currentQuestion.value?.id) return
  try {
    await store.addToWrongQuestions(currentQuestion.value.id)
    isInWrongBookMap.value[currentQuestion.value.id] = true
    ElMessage.success('已加入错题本')
  } catch (error) {
    ElMessage.error('操作失败')
  }
}

const removeFromWrongBook = async () => {
  if (!currentQuestion.value?.id) return
  try {
    const wrongQ = store.wrongQuestions.find(wq => wq.question_id === currentQuestion.value.id)
    if (wrongQ) {
      await store.removeFromWrongQuestions(wrongQ.id)
    }
    isInWrongBookMap.value[currentQuestion.value.id] = false
    ElMessage.success('已移出错题本')
  } catch (error) {
    ElMessage.error('操作失败')
  }
}

const toggleMastered = () => {
  ElMessage.info('已掌握状态标记')
}

const finishPractice = () => {
  let totalQuestions, answeredCount, correctCount, wrongCount, skippedCount, accuracy
  
  if (practiceMode.value === 'memory') {
    // 记忆刷题模式统计
    totalQuestions = memoryTotalCount.value
    answeredCount = memoryCompletedCount.value
    correctCount = memoryCompletedCount.value // 在记忆刷题模式下，完成即代表正确
    wrongCount = 0
    skippedCount = totalQuestions - answeredCount
    accuracy = totalQuestions > 0 ? Math.round((correctCount / totalQuestions) * 100) : 0
  } else {
    totalQuestions = questions.value.length
    answeredCount = Object.keys(answeredQuestions.value).length
    correctCount = Object.values(answeredQuestions.value).filter((answer, idx) => {
      const q = questions.value[idx]
      const correctAnswer = q?.shuffled_options ? (q?.shuffled_answer || '') : (q?.answer || '')
      return correctAnswer.toUpperCase().includes(answer?.toUpperCase())
    }).length
    wrongCount = answeredCount - correctCount
    skippedCount = totalQuestions - answeredCount
    accuracy = answeredCount > 0 ? Math.round((correctCount / answeredCount) * 100) : 0
  }

  let grade = ''
  let gradeIcon = ''
  let gradeColor = ''
  let gradeBgColor = ''
  let encouragement = ''
  let animationClass = ''
  
  if (accuracy >= 90) {
    grade = '优秀'
    gradeIcon = '🏆'
    gradeColor = '#10b981'
    gradeBgColor = 'rgba(16, 185, 129, 0.1)'
    encouragement = '太棒了！继续保持！你的表现非常出色！🎉'
    animationClass = 'excellent'
  } else if (accuracy >= 70) {
    grade = '良好'
    gradeIcon = '👍'
    gradeColor = '#3b82f6'
    gradeBgColor = 'rgba(59, 130, 246, 0.1)'
    encouragement = '表现不错！再接再厉，你可以做得更好！💪'
    animationClass = 'good'
  } else if (accuracy >= 60) {
    grade = '及格'
    gradeIcon = '📚'
    gradeColor = '#f59e0b'
    gradeBgColor = 'rgba(245, 158, 11, 0.1)'
    encouragement = '还需要多加练习！建议复习后再尝试！📖'
    animationClass = 'pass'
  } else {
    grade = '需努力'
    gradeIcon = '💪'
    gradeColor = '#ef4444'
    gradeBgColor = 'rgba(239, 68, 68, 0.1)'
    encouragement = '加油！不要气馁，继续努力你一定能行！✨'
    animationClass = 'fail'
  }

  const modeNames = {
    memorize: '背题模式',
    sequential: '顺序刷题',
    random: '随机出题',
    wrong: '错题练习',
    crazy: '疯狂刷题',
    memory: '记忆刷题'
  }

  const modeColors = {
    memorize: '#8b5cf6',
    sequential: '#06b6d4',
    random: '#f59e0b',
    wrong: '#ef4444',
    crazy: '#ec4899',
    memory: '#10b981'
  }

  const resultHTML = `
    <div class="result-dialog" style="font-family: 'Microsoft YaHei', 'PingFang SC', sans-serif; width: 100%; margin: 0; padding: 0;">
      <div class="result-header" style="background: linear-gradient(135deg, ${modeColors[practiceMode.value] || '#667eea'} 0%, ${modeColors[practiceMode.value] || '#667eea'}dd 100%); padding: 28px 24px; text-align: center;">
        <div class="result-icon" style="font-size: 52px; margin-bottom: 10px; animation: bounce 1s ease infinite;">${gradeIcon}</div>
        <div style="color: white; font-size: 14px; opacity: 0.9; font-weight: 600;">练习完成</div>
      </div>
      
      <div style="padding: 28px 24px; background: white; width: 100%; box-sizing: border-box;">
        <div style="text-align: center; margin-bottom: 28px;">
          <div class="accuracy-display" style="position: relative; display: inline-block;">
            <svg width="140" height="140" style="transform: rotate(-90deg);">
              <circle cx="70" cy="70" r="60" stroke="#e5e7eb" stroke-width="10" fill="none"/>
              <circle cx="70" cy="70" r="60" stroke="${gradeColor}" stroke-width="10" fill="none"
                stroke-dasharray="${2 * Math.PI * 60}" 
                stroke-dashoffset="${2 * Math.PI * 60 * (1 - accuracy / 100)}"
                style="transition: stroke-dashoffset 1s ease-out; stroke-linecap: round;"/>
            </svg>
            <div style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); text-align: center;">
              <div style="font-size: 36px; font-weight: 800; color: ${gradeColor}; line-height: 1;">${accuracy}%</div>
              <div style="font-size: 14px; color: #6b7280; margin-top: 4px;">正确率</div>
            </div>
          </div>
        </div>
        
        <div class="grade-badge" style="display: inline-block; background: ${gradeBgColor}; color: ${gradeColor}; padding: 10px 28px; border-radius: 50px; font-size: 18px; font-weight: 700; margin: 0 auto 24px; display: block; text-align: center; width: fit-content;">
          ${grade}
        </div>
        
        <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; margin-bottom: 24px;">
          <div class="stat-card" style="background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%); padding: 14px 10px; border-radius: 10px; text-align: center; border: 1px solid #bae6fd;">
            <div style="font-size: 22px; font-weight: 700; color: #4f46e5; margin-bottom: 4px;">${totalQuestions}</div>
            <div style="font-size: 11px; color: #6b7280; font-weight: 500;">总题数</div>
          </div>
          <div class="stat-card" style="background: linear-gradient(135deg, #dcfce7 0%, #bbf7d0 100%); padding: 14px 10px; border-radius: 10px; text-align: center; border: 1px solid #86efac;">
            <div style="font-size: 22px; font-weight: 700; color: #10b981; margin-bottom: 4px;">${correctCount}</div>
            <div style="font-size: 11px; color: #6b7280; font-weight: 500;">正确</div>
          </div>
          <div class="stat-card" style="background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%); padding: 14px 10px; border-radius: 10px; text-align: center; border: 1px solid #fca5a5;">
            <div style="font-size: 22px; font-weight: 700; color: #ef4444; margin-bottom: 4px;">${wrongCount}</div>
            <div style="font-size: 11px; color: #6b7280; font-weight: 500;">错误</div>
          </div>
          <div class="stat-card" style="background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%); padding: 14px 10px; border-radius: 10px; text-align: center; border: 1px solid #fcd34d;">
            <div style="font-size: 22px; font-weight: 700; color: #f59e0b; margin-bottom: 4px;">${skippedCount}</div>
            <div style="font-size: 11px; color: #6b7280; font-weight: 500;">跳过</div>
          </div>
        </div>
        
        <div class="tip-card" style="background: linear-gradient(135deg, ${gradeBgColor} 0%, rgba(255,255,255,0.9) 100%); border-left: 4px solid ${gradeColor}; border-radius: 10px; padding: 14px 18px; margin-bottom: 24px;">
          <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 8px;">
            <span style="font-size: 18px;">💡</span>
            <span style="font-size: 14px; font-weight: 600; color: ${gradeColor};">温馨提示</span>
          </div>
          <div style="font-size: 14px; color: #4b5563; line-height: 1.7;">${encouragement}</div>
        </div>
        
        <div class="mode-info" style="background: #f9fafb; border-radius: 10px; padding: 14px 18px; display: flex; align-items: center; justify-content: space-between;">
          <div style="display: flex; align-items: center; gap: 10px;">
            <span style="font-size: 20px;">📝</span>
            <span style="font-size: 14px; font-weight: 600; color: #374151;">练习模式</span>
          </div>
          <span style="font-size: 14px; font-weight: 700; color: ${modeColors[practiceMode.value] || '#667eea'};">${modeNames[practiceMode.value] || '练习'}</span>
        </div>
      </div>
    </div>
    
    <style>
      @keyframes bounce {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-8px); }
      }
      .result-dialog .stat-card {
        transition: all 0.3s ease;
      }
      .result-dialog .stat-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
      }
    </style>
  `

  ElMessageBox.alert(
    resultHTML,
    '',
    { 
      confirmButtonText: '🏠 返回首页', 
      dangerouslyUseHTMLString: true,
      customClass: 'practice-result-dialog-v2',
      showMessageIcon: false
    }
  ).then(() => {
    store.clearSavedPracticeSession(practiceMode.value)
    router.push('/home')
  })
}

const toggleEditMode = async () => {
  isEditMode.value = !isEditMode.value
  if (isEditMode.value) {
    await nextTick()
    if (questionEditorRef.value && currentQuestion.value) {
      questionEditorRef.value.innerHTML = currentQuestion.value.stem_html || currentQuestion.value.stem || ''
    }
  }
}

const toggleExplanationEdit = async () => {
  isExplanationEdit.value = !isExplanationEdit.value
  if (isExplanationEdit.value) {
    await nextTick()
    if (explanationEditorRef.value && currentQuestion.value) {
      explanationEditorRef.value.innerHTML = currentQuestion.value.explanation_html || currentQuestion.value.explanation || ''
    }
  }
}

const formatText = (editor, command, value = null) => {
  if (!editor) return
  editor.focus()
  if (command === 'color') {
    document.execCommand('foreColor', false, value)
  } else if (command.startsWith('highlight-')) {
    const selection = window.getSelection()
    if (selection.rangeCount > 0) {
      const range = selection.getRangeAt(0)
      const span = document.createElement('span')
      span.className = command
      range.surroundContents(span)
    }
  } else {
    document.execCommand(command, false, value)
  }
}

const formatQuestion = (command, value = null) => {
  formatText(questionEditorRef.value, command, value)
}

const formatExplanation = (command, value = null) => {
  formatText(explanationEditorRef.value, command, value)
}

const insertImageQuestion = () => {
  if (!questionEditorRef.value) return
  const url = prompt('请输入图片URL:')
  if (url) {
    document.execCommand('insertImage', false, url)
  }
}

const insertImageExplanation = () => {
  if (!explanationEditorRef.value) return
  const url = prompt('请输入图片URL:')
  if (url) {
    document.execCommand('insertImage', false, url)
  }
}

const insertTableQuestion = () => {
  if (!questionEditorRef.value) return
  const tableHtml = '<table border="1" style="border-collapse: collapse;"><tr><td>单元格</td><td>单元格</td></tr><tr><td>单元格</td><td>单元格</td></tr></table>'
  document.execCommand('insertHTML', false, tableHtml)
}

const insertTableExplanation = () => {
  if (!explanationEditorRef.value) return
  const tableHtml = '<table border="1" style="border-collapse: collapse;"><tr><td>单元格</td><td>单元格</td></tr><tr><td>单元格</td><td>单元格</td></tr></table>'
  document.execCommand('insertHTML', false, tableHtml)
}

const insertFormulaQuestion = () => {
  if (!questionEditorRef.value) return
  const formula = prompt('请输入LaTeX公式:')
  if (formula) {
    const html = `<span class="formula">$$${formula}$$</span>`
    document.execCommand('insertHTML', false, html)
  }
}

const insertFormulaExplanation = () => {
  if (!explanationEditorRef.value) return
  const formula = prompt('请输入LaTeX公式:')
  if (formula) {
    const html = `<span class="formula">$$${formula}$$</span>`
    document.execCommand('insertHTML', false, html)
  }
}

const saveQuestionEdit = async () => {
  if (!currentQuestion.value?.id || !questionEditorRef.value) return
  try {
    await store.updateQuestion(currentQuestion.value.id, {
      stem_html: questionEditorRef.value.innerHTML
    })
    currentQuestion.value.stem_html = questionEditorRef.value.innerHTML
    isEditMode.value = false
    ElMessage.success('题目已更新')
  } catch (error) {
    ElMessage.error('更新失败')
  }
}

const saveExplanationEdit = async () => {
  if (!currentQuestion.value?.id || !explanationEditorRef.value) return
  try {
    await store.updateQuestion(currentQuestion.value.id, {
      explanation_html: explanationEditorRef.value.innerHTML
    })
    currentQuestion.value.explanation_html = explanationEditorRef.value.innerHTML
    isExplanationEdit.value = false
    ElMessage.success('解析已更新')
  } catch (error) {
    ElMessage.error('更新失败')
  }
}

const updateEyeProtection = () => {
  store.updatePreferences({ eye_protection_mode: eyeProtectionMode.value })
}

const updateFontSize = () => {
  store.updatePreferences({ font_size: fontSize.value })
}

const updateFontFamily = () => {
  store.updatePreferences({ font_family: fontFamily.value })
}

const increaseFontSize = () => {
  if (fontSize.value < 40) {
    fontSize.value += 2
    updateFontSize()
  }
}

const decreaseFontSize = () => {
  if (fontSize.value > 8) {
    fontSize.value -= 2
    updateFontSize()
  }
}

onMounted(async () => {
  try {
    await store.loadChapters()
    chapters.value = store.chapters
    await store.loadWrongQuestions({ user_id: store.userId, per_page: 10000 })
    wrongCount.value = store.wrongQuestions.length
    await store.loadQuestions()
    totalQuestions.value = store.questions.length

    const prefs = store.preferences
    eyeProtectionMode.value = prefs.eye_protection_mode || 'none'
    fontSize.value = prefs.font_size || 16
    fontFamily.value = prefs.font_family || 'Microsoft YaHei'

    await nextTick()
    const container = document.querySelector('.practice-layout')
    if (container) {
      const containerRect = container.getBoundingClientRect()
      const handleWidth = 8
      const totalWidth = containerRect.width
      leftPanelWidth.value = Math.max(300, totalWidth * 0.65)
      rightPanelWidth.value = Math.max(250, totalWidth - leftPanelWidth.value - handleWidth)
    }
    
    window.addEventListener('resize', handleWindowResize)
    
    // 初始绑定图片点击事件
    bindImageClickEvents()
    
    // 如果是从章节选择进入错题练习，自动开始练习
    if (practiceMode.value === 'wrong' && (route.query.chapters || route.query.mode === 'wrong_selected')) {
      await startPractice()
    }
    
    // 记忆刷题模式：自动开始加载任务，无需点击开始按钮
    if (practiceMode.value === 'memory') {
      await startPractice()
    }
  } catch (error) {
    console.error('初始化失败:', error)
    ElMessage.error('页面加载失败，请刷新重试')
  }
})

// 监听刷题模式变化，重置组件状态
watch(practiceMode, async (newMode, oldMode) => {
  if (newMode !== oldMode) {
    // 重置所有状态
    questions.value = []
    currentIndex.value = 0
    practiceStarted.value = false
    showAnswer.value = false
    answeredQuestions.value = {}
    isFavorite.value = false
    isInWrongBookMap.value = {}
    totalQuestions.value = store.questions.length
    config.count = 10
    config.chapterIds = []
    isEditMode.value = false
    isExplanationEdit.value = false
    
    // 记忆刷题模式：自动开始加载任务
    if (newMode === 'memory') {
      await startPractice()
    }
  }
})

watch(() => store.preferences, (prefs) => {
  if (prefs) {
    eyeProtectionMode.value = prefs.eye_protection_mode || 'none'
    fontSize.value = prefs.font_size || 16
    fontFamily.value = prefs.font_family || 'Microsoft YaHei'
  }
}, { deep: true })

// 监听题目变化，为图片绑定点击事件
watch(currentQuestion, () => {
  nextTick(() => {
    bindImageClickEvents()
  })
})

const bindImageClickEvents = () => {
  const images = document.querySelectorAll('.question-content img, .option-text img, .explanation-content img')
  images.forEach(img => {
    // 移除之前的事件监听器（避免重复绑定）
    img.style.cursor = 'zoom-in'
    img.onclick = (e) => {
      e.stopPropagation()
      openImagePreview(img.src)
    }
  })
}


// 辨析题相关函数
const openDistinguishDialog = () => {
  const q = currentQuestion.value
  if (!q) return
  distinguishQuestionData.value = {
    id: q.id,
    stem: q.stem,
    stem_html: q.stem_html,
    explanation: q.explanation,
    explanation_html: q.explanation_html
  }
  const optionKeys = ['option_a', 'option_b', 'option_c', 'option_d', 'option_e', 'option_f']
  distinguishOptions.value = []
  for (const key of optionKeys) {
    if (q[key]) {
      distinguishOptions.value.push({
        key: key.replace('option_', '').toUpperCase(),
        text: q[key],
        is_correct: true,
        corrected_text: ''
      })
    }
  }
  showDistinguishDialog.value = true
}

const toggleOptionCorrect = (idx) => {
  distinguishOptions.value[idx].is_correct = !distinguishOptions.value[idx].is_correct
}

const saveDistinguishQuestion = async () => {
  const q = distinguishQuestionData.value
  if (!q) return
  try {
    const { default: axios } = await import('axios')
    await axios.post('/api/distinguish/save', {
      question_id: q.id,
      options: distinguishOptions.value.map(o => ({
        key: o.key,
        text: o.text,
        is_correct: o.is_correct,
        corrected_text: o.is_correct ? null : (o.corrected_text || null)
      }))
    })
    showDistinguishDialog.value = false
    isInDistinguishMap.value[q.id] = true
    alert('已添加到辨析题管理')
  } catch (e) {
    console.error(e)
    alert('保存失败')
  }
}
</script>

<style scoped>
.practice-view {
  padding: 20px;
  min-height: 100vh;
  background: #ffffff; /* 默认白色背景 */
  font-size: 14px; /* 默认字体大小，确保子元素不继承内容区域的字体 */
}

.settings-bar {
  display: flex;
  gap: 20px;
  margin-bottom: 20px;
  padding: 15px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  font-size: 14px !important; /* 强制设置字体大小，不继承 */
}

.settings-bar * {
  font-size: 14px !important; /* 确保设置栏内所有元素都使用固定字体 */
}

.settings-item {
  display: flex;
  align-items: center;
  gap: 10px;
}

.start-screen {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 60vh;
  font-size: 16px;
}

.start-screen * {
  font-size: inherit !important;
}

.start-card {
  background: linear-gradient(135deg, #ffffff 0%, #f9fafb 100%);
  padding: 40px 48px;
  border-radius: 20px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.08), 0 2px 8px rgba(0, 0, 0, 0.04);
  text-align: center;
  max-width: 800px;
  width: 100%;
  box-sizing: border-box;
  border: 1px solid #f3f4f6;
  margin: 0 auto;
}

.start-card h2 {
  font-size: 28px !important;
  font-weight: 800;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin-bottom: 12px;
}

.start-card > p {
  color: #6b7280;
  font-size: 15px;
  margin-bottom: 32px;
}

.start-card .el-button--primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border: none;
  padding: 16px 48px;
  font-size: 16px;
  font-weight: 700;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(102, 126, 234, 0.4);
  transition: all 0.3s ease;
}

.start-card .el-button--primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 30px rgba(102, 126, 234, 0.5);
}

.chapter-select-btn {
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  border: none;
  color: white;
  font-weight: 600;
  padding: 8px 20px;
  border-radius: 8px;
  transition: all 0.2s ease;
}

.chapter-select-btn:hover {
  background: linear-gradient(135deg, #059669 0%, #047857 100%);
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);
}

.chapter-clear-btn {
  background: linear-gradient(135deg, #6b7280 0%, #4b5563 100%);
  border: none;
  color: white;
  font-weight: 600;
  padding: 8px 20px;
  border-radius: 8px;
  transition: all 0.2s ease;
}

.chapter-clear-btn:hover {
  background: linear-gradient(135deg, #4b5563 0%, #374151 100%);
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(75, 85, 99, 0.3);
}

.ratios-label {
  display: block;
  margin-bottom: 12px;
  font-weight: 700;
  color: #0369a1;
  font-size: 14px;
}

.wrong-ratio-label {
  display: block;
  margin-bottom: 12px;
  font-weight: 700;
  color: #92400e;
  font-size: 14px;
}

.config-section {
  margin: 20px 0;
  text-align: left;
  font-size: 14px !important;
}

.config-section * {
  font-size: 14px !important;
}

.config-item {
  margin-bottom: 20px;
}

.config-item:last-child {
  margin-bottom: 0;
}

.config-item label {
  display: block;
  margin-bottom: 10px;
  font-weight: 600;
  color: #374151;
  font-size: 14px;
}

.chapter-select-controls {
  display: flex;
  gap: 14px;
  align-items: center;
  width: 100%;
  box-sizing: border-box;
  flex-wrap: wrap;
}

.chapter-select {
  flex: 1;
  min-width: 250px;
  max-width: 100%;
  box-sizing: border-box;
}

.chapter-select-actions {
  display: flex;
  gap: 10px;
  flex-shrink: 0;
}

.chapter-select-btn,
.chapter-clear-btn {
  white-space: nowrap;
  padding: 10px 20px;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 600;
  transition: all 0.2s ease;
  height: 40px;
}

.chapter-select-btn {
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
  color: white;
  border: none;
}

.chapter-select-btn:hover {
  background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
}

.chapter-clear-btn {
  background: #f3f4f6;
  color: #6b7280;
  border: 1px solid #d1d5db;
}

.chapter-clear-btn:hover {
  background: #e5e7eb;
  color: #374151;
  border-color: #9ca3af;
}

/* 响应式适配 */
@media screen and (max-width: 640px) {
  .chapter-select-controls {
    flex-direction: column;
    align-items: stretch;
  }
  
  .chapter-select {
    min-width: 100%;
  }
  
  .chapter-select-actions {
    justify-content: flex-end;
  }
}

.chapter-ratios-section {
  width: 100%;
  box-sizing: border-box;
  overflow-x: hidden;
  overflow-y: visible;
}

.chapter-ratios {
  background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
  padding: 20px;
  border-radius: 12px;
  margin-top: 16px;
  border: 1px solid #bae6fd;
  width: 100%;
  box-sizing: border-box;
  overflow-x: hidden;
  overflow-y: visible;
}

.chapter-ratio-item {
  margin-bottom: 15px;
  display: flex;
  align-items: center;
  gap: 20px;
  width: 100%;
  box-sizing: border-box;
  padding: 14px 18px;
  background: rgba(255, 255, 255, 0.9);
  border-radius: 10px;
  border: 1px solid #e0f2fe;
  flex-shrink: 0;
}

.chapter-ratio-item:last-child {
  margin-bottom: 0;
}

.chapter-ratio-label {
  flex-shrink: 0;
  min-width: 180px;
  max-width: 250px;
  font-weight: 600;
  color: #0369a1;
  font-size: 14px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  padding: 6px 0;
}

.ratio-input-wrapper {
  display: flex;
  align-items: center;
  gap: 10px;
  flex: 1;
  justify-content: flex-end;
  min-width: 180px;
}

.ratio-input {
  width: 100%;
  max-width: 160px;
  flex-shrink: 0;
}

.ratio-input .el-input-number__decrease,
.ratio-input .el-input-number__increase {
  width: 40px;
  height: 40px;
  font-size: 18px;
}

.ratio-input .el-input-number__input {
  text-align: center;
  font-weight: 600;
  color: #0369a1;
  font-size: 18px;
  width: 60px;
  height: 40px;
}

.ratio-unit {
  font-weight: 600;
  color: #0369a1;
  font-size: 16px;
  flex-shrink: 0;
  padding: 6px 0;
  min-width: 35px;
}

/* 响应式适配 */
@media screen and (max-width: 768px) {
  .chapter-ratios {
    padding: 16px;
  }
  
  .chapter-ratio-item {
    flex-direction: column;
    align-items: stretch;
    gap: 12px;
    padding: 14px;
  }
  
  .chapter-ratio-label {
    min-width: auto;
    max-width: 100%;
    text-align: left;
    white-space: normal;
    overflow: visible;
    text-overflow: clip;
  }
  
  .ratio-input-wrapper {
    justify-content: flex-start;
  }
  
  .ratio-input {
    width: 100%;
    max-width: 180px;
  }
  
  .ratio-input .el-input-number__input {
    font-size: 20px;
    width: 70px;
  }
}

.ratio-summary {
  margin-top: 16px;
  padding: 14px 18px;
  background: linear-gradient(135deg, #dcfce7 0%, #bbf7d0 100%);
  border-radius: 10px;
  color: #166534;
  font-size: 14px;
  font-weight: 600;
  border: 1px solid #86efac;
  width: 100%;
  box-sizing: border-box;
}

.ratio-summary.ratio-error {
  background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%);
  color: #991b1b;
  border-color: #fca5a5;
}

.ratio-summary.ratio-warning {
  background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
  color: #92400e;
  border-color: #fcd34d;
}

.config-grid {
  display: flex;
  flex-direction: column;
  gap: 20px;
  margin-bottom: 24px;
  width: 100%;
  box-sizing: border-box;
}

.config-grid .config-card {
  width: 100%;
  box-sizing: border-box;
}

.config-card {
  background: #ffffff;
  border-radius: 16px;
  border: none;
  overflow: visible;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08), 0 1px 3px rgba(0, 0, 0, 0.06);
  transition: none;
  flex-shrink: 0;
}

.config-card:hover {
  transform: none;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08), 0 1px 3px rgba(0, 0, 0, 0.06);
}

.config-card-header {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 18px 24px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #a855f7 100%);
  color: white;
  font-weight: 700;
  font-size: 15px;
  letter-spacing: 0.3px;
}

.config-card-header .el-icon {
  font-size: 20px;
}

.config-card-body {
  padding: 20px;
  background: #fafbfc;
  width: 100%;
  box-sizing: border-box;
  overflow-x: hidden;
  overflow-y: visible;
  max-height: none;
}

.config-hint {
  font-size: 13px !important;
  color: #6b7280;
  margin-top: 10px;
  padding: 10px 14px;
  background: #f3f4f6;
  border-radius: 8px;
  border-left: 4px solid #9ca3af;
  font-weight: 500;
  width: 100%;
  box-sizing: border-box;
}

.switch-wrapper {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  background: #f9fafb;
  border-radius: 8px;
  border: 1px solid #e5e7eb;
}

.switch-label {
  font-size: 14px;
  color: #4b5563;
  font-weight: 500;
}

.wrong-info-card {
  background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
  border-radius: 12px;
  padding: 18px;
  margin-top: 18px;
  border: 1px solid #fbbf24;
}

.wrong-info-title {
  font-weight: 700;
  color: #92400e;
  margin-bottom: 12px;
  font-size: 14px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.wrong-info-content ul {
  margin: 0;
  padding-left: 20px;
}

.wrong-info-content li {
  margin-bottom: 8px;
  color: #78350f;
  font-size: 13px !important;
  line-height: 1.6;
}

.preview-card {
  background: linear-gradient(135deg, #e0e7ff 0%, #c7d2fe 100%);
  border-radius: 16px;
  padding: 24px;
  border: 1px solid #a5b4fc;
  box-shadow: 0 4px 20px rgba(79, 70, 229, 0.1);
}

.preview-header {
  margin-bottom: 20px;
  display: flex;
  align-items: center;
  gap: 10px;
}

.preview-header h4 {
  margin: 0;
  font-size: 17px;
  color: #3730a3;
  font-weight: 700;
}

.preview-content {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.preview-stat {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 14px 18px;
  background: white;
  border-radius: 10px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  border: 1px solid #e5e7eb;
}

.preview-label {
  font-weight: 600;
  color: #4b5563;
  font-size: 14px;
}

.preview-value {
  font-weight: 700;
  color: #4f46e5;
  font-size: 15px;
}

.preview-chapters {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.chapter-previews {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.chapter-preview {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 18px;
  background: white;
  border-radius: 8px;
  border: 1px solid #e5e7eb;
  transition: all 0.2s ease;
}

.chapter-preview:hover {
  border-color: #a5b4fc;
  transform: translateX(4px);
}

.chapter-name {
  font-weight: 600;
  color: #1f2937;
  font-size: 14px;
}

.chapter-count {
  color: #4f46e5;
  font-weight: 700;
  font-size: 14px;
}

.crazy-rules {
  margin-top: 16px;
  padding: 12px;
  background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
  border-radius: 8px;
  border: 1px solid #fbbf24;
}

.crazy-rules h4 {
  margin: 0 0 8px 0;
  font-size: 14px;
  font-weight: 700;
  color: #92400e;
}

.crazy-rules ul {
  margin: 0;
  padding-left: 20px;
  list-style: none;
}

.crazy-rules li {
  font-size: 13px;
  color: #78350f;
  line-height: 1.6;
  margin-bottom: 4px;
}

.memory-rules {
  margin-top: 12px;
  padding: 16px;
  background: linear-gradient(135deg, #ecfdf5 0%, #d1fae5 100%);
  border-radius: 10px;
  border: 1px solid #10b981;
}

.memory-rules h4 {
  margin: 0 0 12px 0;
  font-size: 15px;
  font-weight: 700;
  color: #065f46;
}

.memory-rules ul {
  margin: 0;
  padding: 0;
  list-style: none;
}

.memory-rules li {
  font-size: 14px;
  color: #047857;
  line-height: 1.8;
  margin-bottom: 6px;
  padding-left: 8px;
  position: relative;
}

.memory-rules li::before {
  content: '';
  position: absolute;
  left: 0;
  top: 50%;
  transform: translateY(-50%);
  width: 4px;
  height: 4px;
  background: #10b981;
  border-radius: 50%;
}

.config-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
  padding-bottom: 18px;
  border-bottom: 2px solid #f3f4f6;
}

.config-header h3 {
  margin: 0;
  font-size: 20px;
  color: #111827;
  font-weight: 700;
  display: flex;
  align-items: center;
  gap: 10px;
}

.config-tip {
  font-size: 13px !important;
  color: #6b7280;
  padding: 8px 14px;
  background: #f3f4f6;
  border-radius: 20px;
  font-weight: 500;
}

.start-card {
  max-width: 1200px;
}

.practice-layout {
  display: flex;
  width: 100%;
  max-width: 100vw;
  overflow: hidden;
  box-sizing: border-box;
  padding: 0;
  margin: 0;
  flex-wrap: nowrap;
}

.practice-left {
  min-width: 280px;
  max-width: calc(100% - 200px);
  flex: 1;
  flex-basis: 60%;
  overflow: hidden;
  box-sizing: border-box;
  position: relative;
}

.practice-right {
  min-width: 200px;
  max-width: calc(100% - 280px);
  flex: 1;
  flex-basis: 40%;
  overflow: hidden;
  box-sizing: border-box;
  position: relative;
}

/* 平板和小屏幕适配 */
@media screen and (max-width: 768px) {
  .practice-layout {
    flex-direction: column;
    height: auto;
  }
  
  .practice-left {
    min-width: 100%;
    max-width: 100%;
    flex-basis: auto;
    flex-shrink: 0;
  }
  
  .practice-right {
    min-width: 100%;
    max-width: 100%;
    flex-basis: auto;
    flex-shrink: 0;
  }
  
  .resize-handle {
    display: none;
  }
}

/* 中等屏幕适配 */
@media screen and (min-width: 769px) and (max-width: 1024px) {
  .practice-left {
    flex-basis: 55%;
    min-width: 250px;
  }
  
  .practice-right {
    flex-basis: 45%;
    min-width: 220px;
  }
}

/* 大屏适配 */
@media screen and (min-width: 1025px) {
  .practice-left {
    flex-basis: 60%;
  }
  
  .practice-right {
    flex-basis: 40%;
  }
}

/* 最强约束：解析框内所有元素都不允许超出 */
.answer-section,
.answer-display,
.explanation-content {
  width: 100% !important;
  max-width: 100% !important;
  overflow: hidden !important;
  box-sizing: border-box !important;
}

/* 终极约束：解析框内的图片必须完全适应 */
.explanation-content img {
  width: 100% !important;
  max-width: 100% !important;
  height: auto !important;
  display: block !important;
  margin: 10px 0 !important;
  box-sizing: border-box !important;
  object-fit: contain !important;
}

.resize-handle {
  width: 16px;
  cursor: col-resize;
  background: transparent;
  transition: background 0.2s;
  flex-shrink: 0;
  position: relative;
  touch-action: none;
  user-select: none;
}

.resize-handle::before {
  content: '';
  position: absolute;
  left: 50%;
  top: 0;
  bottom: 0;
  width: 2px;
  background: #d1d5db;
  transform: translateX(-50%);
  transition: background 0.2s;
}

.resize-handle:hover::before,
.resize-handle:active::before {
  background: #667eea;
}

.resize-handle:hover {
  background: rgba(102, 126, 234, 0.1);
}

.resize-handle:active {
  background: rgba(102, 126, 234, 0.2);
}

/* 触摸优化：增大可触摸区域 */
.resize-handle::after {
  content: '';
  position: absolute;
  left: -8px;
  right: -8px;
  top: 0;
  bottom: 0;
}

.question-area {
  background: white;
  padding: 30px;
  border-radius: 12px;
  box-shadow: 0 4px 16px rgba(0,0,0,0.1);
  font-size: 14px; /* 基础字体大小 */
}

.question-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  font-size: 14px !important;
  gap: 15px;
  flex-wrap: wrap;
}

.question-header .question-type {
  order: 1;
}

.question-header .question-actions {
  order: 2;
}

.question-header .question-navigation {
  order: 3;
  margin-left: auto;
}

.question-header * {
  font-size: 14px !important;
}

.question-type {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 5px 15px;
  border-radius: 20px;
  font-size: 14px !important;
  flex-shrink: 0;
}

.question-actions {
  display: flex;
  gap: 10px;
  flex-shrink: 0;
}

.question-navigation {
  display: flex;
  align-items: center;
  gap: 15px;
  font-size: 14px !important;
  flex-shrink: 0;
}

.question-content {
  line-height: 1.8;
  margin-bottom: 30px;
  /* 字体大小通过内联样式控制，不在这里设置 */
}

.question-loading {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 60px 20px;
  color: #909399;
  font-size: 16px;
  gap: 10px;
}

.question-loading .el-icon {
  font-size: 20px;
}

/* 确保题干内图片完全自适应 */
.question-content img {
  max-width: 100% !important;
  width: 100% !important;
  height: auto !important;
  display: block;
  margin: 10px 0;
  box-sizing: border-box;
}

.options-list {
  margin: 20px 0;
}

.option-item {
  display: flex;
  align-items: center;
  gap: 15px;
  padding: 15px;
  margin: 10px 0;
  border: 3px solid #a3d5a3; /* 更清晰的绿色系边框 */
  border-radius: 10px;
  background: linear-gradient(145deg, #f0fdf0, #e6f7e6); /* 浅绿渐变背景 */
  cursor: pointer;
  transition: all 0.3s;
  font-size: 14px !important;
}

.option-item:hover {
  border-color: #7cb87c;
  background: linear-gradient(145deg, #d4f4d4, #c4ecc4);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(100, 180, 100, 0.2);
}

.option-item.selected {
  border-color: #667eea;
  background: linear-gradient(145deg, #f0f3ff, #e6ebff);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
}

.option-item.correct {
  border-color: #1890ff;
  background: linear-gradient(145deg, #e6f7ff, #d6f0ff);
  box-shadow: 0 4px 12px rgba(24, 144, 255, 0.2);
}

.option-item.wrong {
  border-color: #ff4d4f;
  background: linear-gradient(145deg, #fff0f0, #ffe1e1);
  box-shadow: 0 4px 12px rgba(255, 77, 79, 0.2);
}

.option-label {
  font-weight: bold;
  min-width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #5a5a5a 0%, #3a3a3a 100%);
  color: white;
  border-radius: 50%;
  box-shadow: 0 2px 8px rgba(90, 90, 90, 0.3);
  flex-shrink: 0;
  /* 字体大小通过内联样式控制 */
}

.option-text {
  flex: 1;
  /* 字体大小通过内联样式控制 */
}

.progress {
  font-size: 14px !important;
  font-weight: 500;
}

.question-tabs {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-top: 20px;
  padding: 20px;
  border: 2px solid #e0e0e0;
  border-radius: 12px;
  background: #fafafa;
}

.question-tab {
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 2px solid #e0e0e0;
  border-radius: 50%;
  cursor: pointer;
  transition: all 0.3s;
  font-size: 14px !important;
  font-weight: 500;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.question-tab:hover {
  border-color: #667eea;
  background: #f5f3ff;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.2);
}

.question-tab.active {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-color: transparent;
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
  transform: translateY(-2px);
}

.question-tab.answered {
  border-color: #67c23a;
  background: #f0f9eb;
  color: #67c23a;
}

.question-tab.wrong {
  border-color: #f56c6c;
  background: #fef0f0;
  color: #f56c6c;
}

.answer-section {
  background: white;
  padding: 25px;
  border-radius: 12px;
  box-shadow: 0 4px 16px rgba(0,0,0,0.1);
  height: fit-content;
  overflow: hidden;
  box-sizing: border-box;
  width: 100%;
}

.answer-section .answer-header,
.answer-section .answer-result,
.answer-section .answer-label,
.answer-section .answer-text,
.answer-section .action-buttons,
.answer-section .el-button {
  font-size: 14px !important;
}

.answer-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.answer-header h3 {
  font-size: 18px !important;
}

.answer-display {
  margin-top: 20px;
}

/* 确保解析内容区域的其他样式 */
/* 题干和选项内的图片也保持约束 */
.question-content img,
.option-text img {
  max-width: 100% !important;
  width: auto !important;
  height: auto !important;
  display: inline-block !important;
  margin: 10px 0 !important;
  box-sizing: border-box !important;
}

/* 确保题干、选项、解析内的所有富文本元素都正确继承字体大小 */
.question-content *,
.option-text *,
.explanation-content * {
  font-size: inherit !important;
  font-family: inherit !important;
}

/* 确保加粗、下划线等富文本元素也继承字体大小 */
.question-content b,
.question-content strong,
.question-content u,
.question-content span,
.question-content div,
.option-text b,
.option-text strong,
.option-text u,
.option-text span,
.option-text div,
.explanation-content b,
.explanation-content strong,
.explanation-content u,
.explanation-content span,
.explanation-content div {
  font-size: inherit !important;
  font-family: inherit !important;
}

.answer-result {
  padding: 15px;
  background: #f0f9ff;
  border-radius: 8px;
  margin-bottom: 20px;
}

.answer-label {
  font-weight: 500;
  color: #1890ff;
}

.answer-text {
  font-weight: bold;
  color: #67c23a;
  margin-left: 10px;
}

.explanation-content {
  line-height: 1.8;
  color: #333;
  /* 字体大小通过内联样式控制 */
  overflow: hidden;
  width: 100%;
  max-width: 100%;
  box-sizing: border-box;
  position: relative;
}

.answer-hidden {
  text-align: center;
  padding: 40px;
  color: #999;
}

.action-buttons {
  display: flex;
  gap: 10px;
  margin-top: 20px;
  flex-wrap: wrap;
}

.edit-mode {
  margin: 15px 0;
}

.editor-toolbar {
  display: flex;
  gap: 8px;
  margin-bottom: 10px;
  padding: 10px;
  background: #f5f5f5;
  border-radius: 6px;
  flex-wrap: wrap;
}

.editor-content {
  min-height: 150px;
  padding: 15px;
  border: 1px solid #e0e0e0;
  border-radius: 6px;
  outline: none;
}

.eye-protection-warm {
  background: #fdf6e3;
}

.eye-protection-warm .settings-bar {
  background: #fff9f0;
  border: 2px solid #f0e0c8;
}

.eye-protection-warm .start-card {
  background: #fff9f0;
  border: 2px solid #f0e0c8;
}

.eye-protection-warm .config-section {
  background: #fff5e6;
  padding: 15px;
  border-radius: 8px;
  border: 1px solid #f0e0c8;
}

.eye-protection-warm .question-area {
  background: #fff9f0;
  border: 2px solid #f0e0c8;
}

.eye-protection-warm .question-content,
.eye-protection-warm .option-text,
.eye-protection-warm .explanation-content {
  color: #5a4a3a;
}

.eye-protection-warm .option-item {
  background: #ffffff;
  border: 2px solid #e8d8c8;
}

.eye-protection-warm .option-item:hover {
  background: #fff5e6;
  border-color: #d4a574;
}

.eye-protection-warm .option-label {
  background: linear-gradient(135deg, #8b7355, #6b5344);
}

.eye-protection-warm .answer-section {
  background: #fff9f0;
  border: 2px solid #f0e0c8;
}

.eye-protection-warm .answer-result {
  background: #fff5e6;
  border-left: 4px solid #d4a574;
}

.eye-protection-light {
  background: #f5f5f5;
}

.eye-protection-light .settings-bar {
  background: #ffffff;
  border: 2px solid #e0e0e0;
}

.eye-protection-light .start-card {
  background: #ffffff;
  border: 2px solid #e0e0e0;
}

.eye-protection-light .config-section {
  background: #fafafa;
  padding: 15px;
  border-radius: 8px;
  border: 1px solid #e0e0e0;
}

.eye-protection-light .question-area {
  background: #ffffff;
  border: 2px solid #e0e0e0;
}

.eye-protection-light .question-content,
.eye-protection-light .option-text,
.eye-protection-light .explanation-content {
  color: #333333;
}

.eye-protection-light .option-item {
  background: #ffffff;
  border: 2px solid #d0d0d0;
}

.eye-protection-light .option-item:hover {
  background: #f8f8f8;
  border-color: #909090;
}

.eye-protection-light .option-label {
  background: linear-gradient(135deg, #606060, #404040);
}

.eye-protection-light .answer-section {
  background: #ffffff;
  border: 2px solid #e0e0e0;
}

.eye-protection-light .answer-result {
  background: #f5f5f5;
  border-left: 4px solid #606060;
}

.eye-protection-dark {
  background: #1e1e1e;
}

.eye-protection-dark .settings-bar {
  background: #2a2a2a;
  border: 2px solid #3a3a3a;
}

.eye-protection-dark .start-card {
  background: #2a2a2a;
  border: 2px solid #3a3a3a;
}

.eye-protection-dark .config-section {
  background: #252525;
  padding: 15px;
  border-radius: 8px;
  border: 1px solid #3a3a3a;
}

.eye-protection-dark .question-area {
  background: #2a2a2a;
  border: 2px solid #3a3a3a;
  color: #d4d4d4;
}

.eye-protection-dark .question-content,
.eye-protection-dark .option-text,
.eye-protection-dark .explanation-content {
  color: #d4d4d4;
}

.eye-protection-dark .option-item {
  background: #2d2d2d;
  border: 2px solid #4a4a4a;
  color: #d4d4d4;
}

.eye-protection-dark .option-item:hover {
  background: #353535;
  border-color: #606060;
}

.eye-protection-dark .option-label {
  background: linear-gradient(135deg, #5a5a5a, #3a3a3a);
  color: #d4d4d4;
}

.eye-protection-dark .answer-section {
  background: #2a2a2a;
  border: 2px solid #3a3a3a;
  color: #d4d4d4;
}

.eye-protection-dark .answer-result {
  background: #252525;
  border-left: 4px solid #5a5a5a;
}

.eye-protection-dark .answer-label,
.eye-protection-dark .answer-text {
  color: #d4d4d4;
}

.eye-protection-green {
  background: #c8e4c8;
}

.eye-protection-green .settings-bar {
  background: #d8edd8;
  border: 2px solid #a8d8a8;
}

.eye-protection-green .start-card {
  background: #d8edd8;
  border: 2px solid #a8d8a8;
}

.eye-protection-green .config-section {
  background: #e0f0e0;
  padding: 15px;
  border-radius: 8px;
  border: 1px solid #a8d8a8;
}

.eye-protection-green .question-area {
  background: #d8edd8;
  border: 2px solid #a8d8a8;
  color: #1a3a1a;
}

.eye-protection-green .question-content,
.eye-protection-green .option-text,
.eye-protection-green .explanation-content {
  color: #1a3a1a;
}

.eye-protection-green .option-item {
  background: #e8f5e8;
  border: 2px solid #98d898;
}

.eye-protection-green .option-item:hover {
  background: #d0f0d0;
  border-color: #70c070;
}

.eye-protection-green .option-label {
  background: linear-gradient(135deg, #4a7a4a, #2a5a2a);
}

.eye-protection-green .answer-section {
  background: #d8edd8;
  border: 2px solid #a8d8a8;
  color: #1a3a1a;
}

.eye-protection-green .answer-result {
  background: #e8f5e8;
  border-left: 4px solid #70c070;
}

.eye-protection-green .answer-label {
  color: #2a6a2a;
}

.eye-protection-green .answer-text {
  color: #1a5a1a;
}

.eye-protection-green .question-area,
.eye-protection-green .answer-section {
  background: rgb(207, 232, 204);
  color: #000000;
}

.eye-protection-green .question-content,
.eye-protection-green .explanation-content {
  color: #000000;
}

.eye-protection-green .option-item.correct {
  border: 4px solid #1890ff !important;
  background: linear-gradient(145deg, #e6f7ff, #d6f0ff) !important;
  box-shadow: 0 0 20px rgba(24, 144, 255, 0.4), inset 0 0 15px rgba(24, 144, 255, 0.2) !important;
  transform: scale(1.02);
}

.eye-protection-green .option-label {
  background: linear-gradient(135deg, #5a5a5a, #3a3a3a) !important;
  box-shadow: 0 3px 10px rgba(90, 90, 90, 0.4) !important;
}

.highlight-yellow {
  background: #FFF176;
  padding: 2px 4px;
  border-radius: 3px;
}

.highlight-green {
  background: #A5D6A7;
  padding: 2px 4px;
  border-radius: 3px;
}

/* 图片预览样式 */
.image-preview-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.8);
  z-index: 9999;
  display: flex;
  justify-content: center;
  align-items: center;
  cursor: zoom-out;
}

.image-preview-container {
  position: relative;
  max-width: 90vw;
  max-height: 90vh;
  background: white;
  border-radius: 8px;
  overflow: hidden;
  cursor: default;
}

.image-preview-close {
  position: absolute;
  top: 10px;
  right: 15px;
  font-size: 32px;
  color: white;
  cursor: pointer;
  z-index: 10;
  text-shadow: 0 0 5px rgba(0, 0, 0, 0.5);
  line-height: 1;
}

.image-preview-close:hover {
  color: #ff6b6b;
}

.image-preview-img {
  max-width: 100%;
  max-height: 90vh;
  display: block;
  width: auto;
  height: auto;
  object-fit: contain;
}

/* 错题练习模块特殊样式 */
.practiceMode-wrong .start-card {
  background: linear-gradient(135deg, #fff7ed 0%, #ffedd5 100%);
  border-color: #fed7aa;
}

.practiceMode-wrong .start-card h2 {
  background: linear-gradient(135deg, #ea580c 0%, #c2410c 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.practiceMode-wrong .start-card .el-button--primary {
  background: linear-gradient(135deg, #ea580c 0%, #c2410c 100%);
  box-shadow: 0 4px 20px rgba(234, 88, 12, 0.4);
}

.practiceMode-wrong .start-card .el-button--primary:hover {
  box-shadow: 0 8px 30px rgba(234, 88, 12, 0.5);
}

.practiceMode-wrong .config-section {
  background: rgba(255, 255, 255, 0.95);
  padding: 24px;
  border-radius: 16px;
  border: 1px solid #fed7aa;
  box-shadow: 0 4px 16px rgba(234, 88, 12, 0.1);
}

.practiceMode-wrong .config-item {
  margin-bottom: 20px;
}

.practiceMode-wrong .config-item:last-child {
  margin-bottom: 0;
}

.practiceMode-wrong .config-item label {
  color: #9a3412;
  font-weight: 700;
  font-size: 15px;
  display: block;
  margin-bottom: 10px;
}

.practiceMode-wrong .config-item .el-select {
  width: 100%;
}

.practiceMode-wrong .config-hint {
  background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
  padding: 12px 16px;
  border-radius: 8px;
  margin-top: 12px;
  color: #92400e;
  font-size: 13px !important;
  font-weight: 600;
  border-left: 4px solid #f59e0b;
}
</style>

<style>
.practice-result-dialog-v2 {
  max-width: 520px !important;
  border-radius: 16px !important;
  padding: 0 !important;
  overflow: hidden !important;
}

.practice-result-dialog-v2 .el-message-box__header {
  display: none !important;
}

.practice-result-dialog-v2 .el-message-box__content {
  padding: 0 !important;
  margin: 0 !important;
}

.practice-result-dialog-v2 .el-message-box__container {
  padding: 0 !important;
  display: block !important;
}

.practice-result-dialog-v2 .el-message-box__status {
  display: none !important;
}

.practice-result-dialog-v2 .el-message-box__message {
  padding: 0 !important;
}

.practice-result-dialog-v2 .el-message-box__message > p {
  margin: 0 !important;
  padding: 0 !important;
}

.practice-result-dialog-v2 .el-message-box__message .el-message-box__content {
  padding: 0 !important;
}

.practice-result-dialog-v2 .el-message-box__btns {
  padding: 20px 24px !important;
  border-top: none !important;
  background: white !important;
}

.practice-result-dialog-v2 .el-button--primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
  border: none !important;
  padding: 14px 36px !important;
  font-size: 16px !important;
  font-weight: 600 !important;
  border-radius: 10px !important;
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3) !important;
  width: 100% !important;
  transition: all 0.3s ease !important;
}

.practice-result-dialog-v2 .el-button--primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(102, 126, 234, 0.4) !important;
  background: linear-gradient(135deg, #7c8ff5 0%, #8a5db8 100%) !important;
}

/* 辨析题弹窗样式 */
.distinguish-dialog-container {
  border-radius: 16px !important;
  overflow: hidden !important;
}

.distinguish-dialog-container .el-dialog__body {
  padding: 0 !important;
  max-height: 85vh;
  overflow-y: auto;
}

.distinguish-dialog {
  padding: 0;
}

.distinguish-dialog .dialog-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 24px 32px;
  display: flex;
  align-items: center;
  gap: 16px;
}

.distinguish-dialog .dialog-icon {
  width: 56px;
  height: 56px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  flex-shrink: 0;
}

.distinguish-dialog .dialog-title-section h3 {
  color: white;
  font-size: 20px;
  font-weight: 600;
  margin: 0 0 6px 0;
}

.distinguish-dialog .dialog-subtitle {
  color: rgba(255, 255, 255, 0.85);
  font-size: 14px;
  margin: 0;
}

.distinguish-dialog .dialog-content {
  padding: 24px 32px;
}

.distinguish-dialog .stem-card {
  background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
  border-radius: 12px;
  padding: 20px;
  margin-bottom: 24px;
  border: 1px solid #e2e8f0;
}

.distinguish-dialog .stem-label {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #64748b;
  font-size: 13px;
  font-weight: 600;
  margin-bottom: 12px;
}

.distinguish-dialog .stem-content {
  font-size: 16px;
  line-height: 1.8;
  color: #1e293b;
}

.distinguish-dialog .options-section {
  margin-bottom: 24px;
}

.distinguish-dialog .options-label {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #475569;
  font-size: 15px;
  font-weight: 600;
  margin-bottom: 16px;
}

.distinguish-dialog .option-card {
  background: white;
  border-radius: 12px;
  padding: 20px;
  margin-bottom: 16px;
  border: 2px solid #e2e8f0;
  transition: all 0.3s ease;
}

.distinguish-dialog .option-card:hover {
  border-color: #cbd5e1;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

.distinguish-dialog .option-card.wrong {
  border-color: #fecaca;
  background: #fef2f2;
}

.distinguish-dialog .option-header {
  display: flex;
  align-items: center;
  gap: 12px;
}

.distinguish-dialog .option-key {
  font-weight: 700;
  font-size: 16px;
  color: #334155;
  min-width: 28px;
}

.distinguish-dialog .option-text {
  flex: 1;
  font-size: 15px;
  line-height: 1.6;
  color: #1e293b;
}

.distinguish-dialog .toggle-btn {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 16px;
  border-radius: 20px;
  font-size: 14px;
  font-weight: 600;
  border: none;
  cursor: pointer;
  transition: all 0.3s ease;
}

.distinguish-dialog .toggle-btn.correct {
  background: linear-gradient(135deg, #86efac 0%, #4ade80 100%);
  color: #166534;
}

.distinguish-dialog .toggle-btn.correct:hover {
  transform: scale(1.05);
  box-shadow: 0 4px 12px rgba(74, 222, 128, 0.4);
}

.distinguish-dialog .toggle-btn.wrong {
  background: linear-gradient(135deg, #fca5a5 0%, #f87171 100%);
  color: #991b1b;
}

.distinguish-dialog .toggle-btn.wrong:hover {
  transform: scale(1.05);
  box-shadow: 0 4px 12px rgba(248, 113, 113, 0.4);
}

.distinguish-dialog .corrected-input-section {
  margin-top: 16px;
  padding-top: 16px;
  border-top: 1px dashed #fecaca;
}

.distinguish-dialog .corrected-label {
  display: flex;
  align-items: center;
  gap: 6px;
  color: #dc2626;
  font-size: 13px;
  font-weight: 600;
  margin-bottom: 10px;
}

.distinguish-dialog .explanation-card {
  background: linear-gradient(135deg, #fefce8 0%, #fef9c3 100%);
  border-radius: 12px;
  padding: 20px;
  border: 1px solid #fde68a;
}

.distinguish-dialog .explanation-label {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #92400e;
  font-size: 13px;
  font-weight: 600;
  margin-bottom: 12px;
}

.distinguish-dialog .explanation-content {
  font-size: 14px;
  line-height: 1.7;
  color: #78350f;
}

.distinguish-dialog .dialog-footer {
  padding: 16px 32px 24px;
  display: flex;
  gap: 16px;
  justify-content: flex-end;
}

.distinguish-dialog .cancel-btn {
  padding: 12px 32px;
  font-size: 15px;
  font-weight: 500;
  border-radius: 10px;
}

.distinguish-dialog .save-btn {
  padding: 12px 40px;
  font-size: 15px;
  font-weight: 600;
  border-radius: 10px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
  border: none !important;
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
  transition: all 0.3s ease;
}

.distinguish-dialog .save-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(102, 126, 234, 0.4);
}
</style>
