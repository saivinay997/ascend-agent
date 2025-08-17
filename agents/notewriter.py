"""
Notewriter Agent for the Ascend system.

The Notewriter Agent processes academic content and generates tailored study materials
that match individual learning styles and preferences.
"""

import asyncio
from typing import Any, Dict, List, Optional
from datetime import datetime
from dataclasses import dataclass

from .base_agent import BaseAgent, AgentResponse
from config.logging_config import LoggerMixin


@dataclass
class StudyMaterial:
    """Represents a study material."""
    title: str
    content: str
    material_type: str  # notes, summary, quiz, flashcards, etc.
    subject: str
    learning_style: str
    difficulty_level: str
    estimated_duration: int  # minutes
    tags: List[str]
    created_at: datetime


@dataclass
class ContentAnalysis:
    """Represents analysis of academic content."""
    key_concepts: List[str]
    difficulty_level: str
    estimated_study_time: int
    prerequisites: List[str]
    learning_objectives: List[str]
    suggested_activities: List[str]


class NotewriterAgent(BaseAgent):
    """
    Notewriter Agent - Academic content processing and study material generation specialist.
    
    Responsibilities:
    - Process and analyze academic content
    - Generate personalized study materials
    - Create summaries, notes, and study guides
    - Generate quizzes and practice questions
    - Adapt content to different learning styles
    - Create visual aids and diagrams
    """
    
    def __init__(self, **kwargs):
        """Initialize the Notewriter Agent."""
        super().__init__(
            name="Notewriter",
            description="Academic content processing and study material generation specialist",
            **kwargs
        )
        self.material_database = {}
        self.content_analyses = {}
        self.learning_style_templates = {
            "visual": {
                "preferred_formats": ["diagrams", "mind_maps", "infographics", "charts"],
                "content_structure": "hierarchical",
                "emphasis": "visual_organization"
            },
            "auditory": {
                "preferred_formats": ["audio_summaries", "discussions", "explanations"],
                "content_structure": "narrative",
                "emphasis": "verbal_explanation"
            },
            "kinesthetic": {
                "preferred_formats": ["interactive_exercises", "hands_on_activities", "simulations"],
                "content_structure": "experiential",
                "emphasis": "practical_application"
            },
            "reading": {
                "preferred_formats": ["detailed_notes", "comprehensive_texts", "reading_lists"],
                "content_structure": "detailed",
                "emphasis": "comprehensive_coverage"
            }
        }
        
    async def process_task(
        self, 
        task: Dict[str, Any], 
        context: Optional[Dict[str, Any]] = None
    ) -> AgentResponse:
        """
        Process a content creation task.
        
        Args:
            task: Task to process
            context: Additional context
            
        Returns:
            AgentResponse with the result
        """
        task_type = task.get("type", "unknown")
        
        if task_type == "analyze_content":
            return await self._analyze_content(task, context)
        elif task_type == "generate_notes":
            return await self._generate_notes(task, context)
        elif task_type == "create_summary":
            return await self._create_summary(task, context)
        elif task_type == "generate_quiz":
            return await self._generate_quiz(task, context)
        elif task_type == "create_flashcards":
            return await self._create_flashcards(task, context)
        elif task_type == "adapt_content":
            return await self._adapt_content(task, context)
        elif task_type == "create_visual_aids":
            return await self._create_visual_aids(task, context)
        else:
            return await self._handle_unknown_task(task, context)
    
    async def _analyze_content(
        self, 
        task: Dict[str, Any], 
        context: Optional[Dict[str, Any]] = None
    ) -> AgentResponse:
        """Analyze academic content to understand structure and requirements."""
        content = task.get("content", "")
        subject = task.get("subject", "")
        student_id = task.get("student_id", "")
        
        if not content:
            return AgentResponse(
                content="",
                metadata={"task": task},
                success=False,
                error="Content is required for analysis"
            )
        
        try:
            # Analyze content structure and complexity
            analysis = await self._perform_content_analysis(content, subject)
            
            # Store analysis for future reference
            content_key = f"{student_id}_{subject}_{datetime.now().isoformat()}"
            self.content_analyses[content_key] = analysis
            
            analysis_summary = self._generate_analysis_summary(analysis)
            
            return AgentResponse(
                content=analysis_summary,
                metadata={
                    "student_id": student_id,
                    "subject": subject,
                    "analysis": analysis,
                    "content_key": content_key
                },
                success=True
            )
            
        except Exception as e:
            self.logger.error(
                "Content analysis failed",
                student_id=student_id,
                subject=subject,
                error=str(e)
            )
            return AgentResponse(
                content="",
                metadata={"student_id": student_id, "subject": subject},
                success=False,
                error=str(e)
            )
    
    async def _generate_notes(
        self, 
        task: Dict[str, Any], 
        context: Optional[Dict[str, Any]] = None
    ) -> AgentResponse:
        """Generate personalized notes based on content and learning style."""
        content = task.get("content", "")
        subject = task.get("subject", "")
        learning_style = task.get("learning_style", "visual")
        student_id = task.get("student_id", "")
        
        if not content or not subject:
            return AgentResponse(
                content="",
                metadata={"task": task},
                success=False,
                error="Content and subject are required"
            )
        
        try:
            # Analyze content first
            analysis = await self._perform_content_analysis(content, subject)
            
            # Generate notes based on learning style
            notes_content = await self._create_style_specific_notes(
                content, analysis, learning_style
            )
            
            # Create study material object
            study_material = StudyMaterial(
                title=f"{subject} Notes",
                content=notes_content,
                material_type="notes",
                subject=subject,
                learning_style=learning_style,
                difficulty_level=analysis.difficulty_level,
                estimated_duration=analysis.estimated_study_time,
                tags=analysis.key_concepts,
                created_at=datetime.now()
            )
            
            # Store material
            if student_id not in self.material_database:
                self.material_database[student_id] = []
            self.material_database[student_id].append(study_material)
            
            return AgentResponse(
                content=notes_content,
                metadata={
                    "student_id": student_id,
                    "subject": subject,
                    "learning_style": learning_style,
                    "material": {
                        "title": study_material.title,
                        "type": study_material.material_type,
                        "duration": study_material.estimated_duration
                    }
                },
                success=True
            )
            
        except Exception as e:
            self.logger.error(
                "Note generation failed",
                student_id=student_id,
                subject=subject,
                error=str(e)
            )
            return AgentResponse(
                content="",
                metadata={"student_id": student_id, "subject": subject},
                success=False,
                error=str(e)
            )
    
    async def _create_summary(
        self, 
        task: Dict[str, Any], 
        context: Optional[Dict[str, Any]] = None
    ) -> AgentResponse:
        """Create a comprehensive summary of academic content."""
        content = task.get("content", "")
        subject = task.get("subject", "")
        summary_type = task.get("summary_type", "comprehensive")  # brief, comprehensive, key_points
        student_id = task.get("student_id", "")
        
        if not content or not subject:
            return AgentResponse(
                content="",
                metadata={"task": task},
                success=False,
                error="Content and subject are required"
            )
        
        try:
            # Analyze content
            analysis = await self._perform_content_analysis(content, subject)
            
            # Generate summary based on type
            if summary_type == "brief":
                summary_content = await self._create_brief_summary(content, analysis)
            elif summary_type == "key_points":
                summary_content = await self._create_key_points_summary(content, analysis)
            else:  # comprehensive
                summary_content = await self._create_comprehensive_summary(content, analysis)
            
            # Create study material
            study_material = StudyMaterial(
                title=f"{subject} {summary_type.title()} Summary",
                content=summary_content,
                material_type="summary",
                subject=subject,
                learning_style="mixed",
                difficulty_level=analysis.difficulty_level,
                estimated_duration=analysis.estimated_study_time // 2,  # Summaries take less time
                tags=analysis.key_concepts,
                created_at=datetime.now()
            )
            
            # Store material
            if student_id not in self.material_database:
                self.material_database[student_id] = []
            self.material_database[student_id].append(study_material)
            
            return AgentResponse(
                content=summary_content,
                metadata={
                    "student_id": student_id,
                    "subject": subject,
                    "summary_type": summary_type,
                    "material": {
                        "title": study_material.title,
                        "type": study_material.material_type,
                        "duration": study_material.estimated_duration
                    }
                },
                success=True
            )
            
        except Exception as e:
            self.logger.error(
                "Summary creation failed",
                student_id=student_id,
                subject=subject,
                error=str(e)
            )
            return AgentResponse(
                content="",
                metadata={"student_id": student_id, "subject": subject},
                success=False,
                error=str(e)
            )
    
    async def _generate_quiz(
        self, 
        task: Dict[str, Any], 
        context: Optional[Dict[str, Any]] = None
    ) -> AgentResponse:
        """Generate quiz questions based on content."""
        content = task.get("content", "")
        subject = task.get("subject", "")
        question_types = task.get("question_types", ["multiple_choice", "true_false"])
        num_questions = task.get("num_questions", 10)
        student_id = task.get("student_id", "")
        
        if not content or not subject:
            return AgentResponse(
                content="",
                metadata={"task": task},
                success=False,
                error="Content and subject are required"
            )
        
        try:
            # Analyze content
            analysis = await self._perform_content_analysis(content, subject)
            
            # Generate questions
            quiz_content = await self._create_quiz_questions(
                content, analysis, question_types, num_questions
            )
            
            # Create study material
            study_material = StudyMaterial(
                title=f"{subject} Practice Quiz",
                content=quiz_content,
                material_type="quiz",
                subject=subject,
                learning_style="mixed",
                difficulty_level=analysis.difficulty_level,
                estimated_duration=num_questions * 2,  # 2 minutes per question
                tags=analysis.key_concepts,
                created_at=datetime.now()
            )
            
            # Store material
            if student_id not in self.material_database:
                self.material_database[student_id] = []
            self.material_database[student_id].append(study_material)
            
            return AgentResponse(
                content=quiz_content,
                metadata={
                    "student_id": student_id,
                    "subject": subject,
                    "question_types": question_types,
                    "num_questions": num_questions,
                    "material": {
                        "title": study_material.title,
                        "type": study_material.material_type,
                        "duration": study_material.estimated_duration
                    }
                },
                success=True
            )
            
        except Exception as e:
            self.logger.error(
                "Quiz generation failed",
                student_id=student_id,
                subject=subject,
                error=str(e)
            )
            return AgentResponse(
                content="",
                metadata={"student_id": student_id, "subject": subject},
                success=False,
                error=str(e)
            )
    
    async def _create_flashcards(
        self, 
        task: Dict[str, Any], 
        context: Optional[Dict[str, Any]] = None
    ) -> AgentResponse:
        """Create flashcards for key concepts."""
        content = task.get("content", "")
        subject = task.get("subject", "")
        num_cards = task.get("num_cards", 20)
        student_id = task.get("student_id", "")
        
        if not content or not subject:
            return AgentResponse(
                content="",
                metadata={"task": task},
                success=False,
                error="Content and subject are required"
            )
        
        try:
            # Analyze content
            analysis = await self._perform_content_analysis(content, subject)
            
            # Generate flashcards
            flashcard_content = await self._create_flashcard_set(
                content, analysis, num_cards
            )
            
            # Create study material
            study_material = StudyMaterial(
                title=f"{subject} Flashcards",
                content=flashcard_content,
                material_type="flashcards",
                subject=subject,
                learning_style="mixed",
                difficulty_level=analysis.difficulty_level,
                estimated_duration=num_cards * 1,  # 1 minute per card
                tags=analysis.key_concepts,
                created_at=datetime.now()
            )
            
            # Store material
            if student_id not in self.material_database:
                self.material_database[student_id] = []
            self.material_database[student_id].append(study_material)
            
            return AgentResponse(
                content=flashcard_content,
                metadata={
                    "student_id": student_id,
                    "subject": subject,
                    "num_cards": num_cards,
                    "material": {
                        "title": study_material.title,
                        "type": study_material.material_type,
                        "duration": study_material.estimated_duration
                    }
                },
                success=True
            )
            
        except Exception as e:
            self.logger.error(
                "Flashcard creation failed",
                student_id=student_id,
                subject=subject,
                error=str(e)
            )
            return AgentResponse(
                content="",
                metadata={"student_id": student_id, "subject": subject},
                success=False,
                error=str(e)
            )
    
    async def _adapt_content(
        self, 
        task: Dict[str, Any], 
        context: Optional[Dict[str, Any]] = None
    ) -> AgentResponse:
        """Adapt existing content to different learning styles."""
        original_content = task.get("original_content", "")
        target_learning_style = task.get("target_learning_style", "visual")
        subject = task.get("subject", "")
        student_id = task.get("student_id", "")
        
        if not original_content or not target_learning_style:
            return AgentResponse(
                content="",
                metadata={"task": task},
                success=False,
                error="Original content and target learning style are required"
            )
        
        try:
            # Analyze original content
            analysis = await self._perform_content_analysis(original_content, subject)
            
            # Adapt content to target learning style
            adapted_content = await self._adapt_to_learning_style(
                original_content, analysis, target_learning_style
            )
            
            # Create study material
            study_material = StudyMaterial(
                title=f"{subject} ({target_learning_style.title()} Style)",
                content=adapted_content,
                material_type="adapted_content",
                subject=subject,
                learning_style=target_learning_style,
                difficulty_level=analysis.difficulty_level,
                estimated_duration=analysis.estimated_study_time,
                tags=analysis.key_concepts,
                created_at=datetime.now()
            )
            
            # Store material
            if student_id not in self.material_database:
                self.material_database[student_id] = []
            self.material_database[student_id].append(study_material)
            
            return AgentResponse(
                content=adapted_content,
                metadata={
                    "student_id": student_id,
                    "subject": subject,
                    "target_learning_style": target_learning_style,
                    "material": {
                        "title": study_material.title,
                        "type": study_material.material_type,
                        "duration": study_material.estimated_duration
                    }
                },
                success=True
            )
            
        except Exception as e:
            self.logger.error(
                "Content adaptation failed",
                student_id=student_id,
                subject=subject,
                error=str(e)
            )
            return AgentResponse(
                content="",
                metadata={"student_id": student_id, "subject": subject},
                success=False,
                error=str(e)
            )
    
    async def _create_visual_aids(
        self, 
        task: Dict[str, Any], 
        context: Optional[Dict[str, Any]] = None
    ) -> AgentResponse:
        """Create visual aids and diagrams for content."""
        content = task.get("content", "")
        subject = task.get("subject", "")
        visual_type = task.get("visual_type", "mind_map")  # mind_map, diagram, chart, infographic
        student_id = task.get("student_id", "")
        
        if not content or not subject:
            return AgentResponse(
                content="",
                metadata={"task": task},
                success=False,
                error="Content and subject are required"
            )
        
        try:
            # Analyze content
            analysis = await self._perform_content_analysis(content, subject)
            
            # Generate visual aid description
            visual_content = await self._generate_visual_description(
                content, analysis, visual_type
            )
            
            # Create study material
            study_material = StudyMaterial(
                title=f"{subject} {visual_type.replace('_', ' ').title()}",
                content=visual_content,
                material_type="visual_aid",
                subject=subject,
                learning_style="visual",
                difficulty_level=analysis.difficulty_level,
                estimated_duration=analysis.estimated_study_time // 3,  # Visuals are faster to process
                tags=analysis.key_concepts,
                created_at=datetime.now()
            )
            
            # Store material
            if student_id not in self.material_database:
                self.material_database[student_id] = []
            self.material_database[student_id].append(study_material)
            
            return AgentResponse(
                content=visual_content,
                metadata={
                    "student_id": student_id,
                    "subject": subject,
                    "visual_type": visual_type,
                    "material": {
                        "title": study_material.title,
                        "type": study_material.material_type,
                        "duration": study_material.estimated_duration
                    }
                },
                success=True
            )
            
        except Exception as e:
            self.logger.error(
                "Visual aid creation failed",
                student_id=student_id,
                subject=subject,
                error=str(e)
            )
            return AgentResponse(
                content="",
                metadata={"student_id": student_id, "subject": subject},
                success=False,
                error=str(e)
            )
    
    async def _perform_content_analysis(
        self, 
        content: str, 
        subject: str
    ) -> ContentAnalysis:
        """Perform comprehensive analysis of academic content."""
        # This would use the LLM to analyze content
        # For now, we'll create a simplified analysis
        
        # Extract key concepts (simplified)
        key_concepts = self._extract_key_concepts(content)
        
        # Determine difficulty level
        difficulty_level = self._assess_difficulty(content)
        
        # Estimate study time
        estimated_study_time = self._estimate_study_time(content, difficulty_level)
        
        # Identify prerequisites
        prerequisites = self._identify_prerequisites(content, subject)
        
        # Define learning objectives
        learning_objectives = self._define_learning_objectives(content, subject)
        
        # Suggest activities
        suggested_activities = self._suggest_activities(content, subject, difficulty_level)
        
        return ContentAnalysis(
            key_concepts=key_concepts,
            difficulty_level=difficulty_level,
            estimated_study_time=estimated_study_time,
            prerequisites=prerequisites,
            learning_objectives=learning_objectives,
            suggested_activities=suggested_activities
        )
    
    async def _create_style_specific_notes(
        self, 
        content: str, 
        analysis: ContentAnalysis, 
        learning_style: str
    ) -> str:
        """Create notes tailored to a specific learning style."""
        template = self.learning_style_templates.get(learning_style, {})
        
        # Use LLM to generate style-specific notes
        prompt = f"""
        Create comprehensive notes for the following content, tailored for {learning_style} learners.
        
        Content: {content}
        
        Key concepts: {', '.join(analysis.key_concepts)}
        Learning objectives: {', '.join(analysis.learning_objectives)}
        
        Preferred format: {template.get('preferred_formats', ['text'])}
        Content structure: {template.get('content_structure', 'standard')}
        Emphasis: {template.get('emphasis', 'comprehensive')}
        
        Please create detailed, well-organized notes that are optimized for {learning_style} learners.
        """
        
        response = await self.process_message(prompt)
        return response.content if response.success else "Failed to generate notes"
    
    async def _create_brief_summary(
        self, 
        content: str, 
        analysis: ContentAnalysis
    ) -> str:
        """Create a brief summary of the content."""
        prompt = f"""
        Create a brief, concise summary of the following content in 2-3 paragraphs.
        
        Content: {content}
        
        Key concepts: {', '.join(analysis.key_concepts)}
        
        Focus on the most important points and main ideas.
        """
        
        response = await self.process_message(prompt)
        return response.content if response.success else "Failed to generate summary"
    
    async def _create_comprehensive_summary(
        self, 
        content: str, 
        analysis: ContentAnalysis
    ) -> str:
        """Create a comprehensive summary of the content."""
        prompt = f"""
        Create a comprehensive summary of the following content.
        
        Content: {content}
        
        Key concepts: {', '.join(analysis.key_concepts)}
        Learning objectives: {', '.join(analysis.learning_objectives)}
        
        Include all important details, examples, and connections between concepts.
        """
        
        response = await self.process_message(prompt)
        return response.content if response.success else "Failed to generate summary"
    
    async def _create_key_points_summary(
        self, 
        content: str, 
        analysis: ContentAnalysis
    ) -> str:
        """Create a key points summary."""
        prompt = f"""
        Create a key points summary of the following content using bullet points.
        
        Content: {content}
        
        Key concepts: {', '.join(analysis.key_concepts)}
        
        Present the main ideas and key points in a clear, organized bullet-point format.
        """
        
        response = await self.process_message(prompt)
        return response.content if response.success else "Failed to generate summary"
    
    async def _create_quiz_questions(
        self, 
        content: str, 
        analysis: ContentAnalysis, 
        question_types: List[str], 
        num_questions: int
    ) -> str:
        """Create quiz questions based on content."""
        prompt = f"""
        Create {num_questions} quiz questions based on the following content.
        
        Content: {content}
        
        Key concepts: {', '.join(analysis.key_concepts)}
        Question types: {', '.join(question_types)}
        
        Include a mix of question types and difficulty levels. Provide clear, correct answers.
        """
        
        response = await self.process_message(prompt)
        return response.content if response.success else "Failed to generate quiz"
    
    async def _create_flashcard_set(
        self, 
        content: str, 
        analysis: ContentAnalysis, 
        num_cards: int
    ) -> str:
        """Create flashcards for key concepts."""
        prompt = f"""
        Create {num_cards} flashcards based on the following content.
        
        Content: {content}
        
        Key concepts: {', '.join(analysis.key_concepts)}
        
        Format each flashcard as:
        Front: [Question/Concept]
        Back: [Answer/Explanation]
        
        Focus on the most important concepts and definitions.
        """
        
        response = await self.process_message(prompt)
        return response.content if response.success else "Failed to generate flashcards"
    
    async def _adapt_to_learning_style(
        self, 
        content: str, 
        analysis: ContentAnalysis, 
        target_style: str
    ) -> str:
        """Adapt content to a specific learning style."""
        template = self.learning_style_templates.get(target_style, {})
        
        prompt = f"""
        Adapt the following content for {target_style} learners.
        
        Original content: {content}
        
        Key concepts: {', '.join(analysis.key_concepts)}
        Target learning style: {target_style}
        Preferred formats: {', '.join(template.get('preferred_formats', []))}
        Content structure: {template.get('content_structure', 'standard')}
        Emphasis: {template.get('emphasis', 'comprehensive')}
        
        Transform the content to be optimal for {target_style} learners while maintaining all important information.
        """
        
        response = await self.process_message(prompt)
        return response.content if response.success else "Failed to adapt content"
    
    async def _generate_visual_description(
        self, 
        content: str, 
        analysis: ContentAnalysis, 
        visual_type: str
    ) -> str:
        """Generate description for visual aids."""
        prompt = f"""
        Create a detailed description for a {visual_type} based on the following content.
        
        Content: {content}
        
        Key concepts: {', '.join(analysis.key_concepts)}
        Visual type: {visual_type}
        
        Provide a detailed description of how to create this visual aid, including:
        - Main elements and their relationships
        - Layout and organization
        - Key information to include
        - Visual hierarchy and emphasis
        """
        
        response = await self.process_message(prompt)
        return response.content if response.success else "Failed to generate visual description"
    
    def _extract_key_concepts(self, content: str) -> List[str]:
        """Extract key concepts from content."""
        # Simplified implementation - in reality, this would use NLP
        words = content.split()
        # Return first 10 unique words as "concepts"
        return list(set(words[:10]))
    
    def _assess_difficulty(self, content: str) -> str:
        """Assess the difficulty level of content."""
        # Simplified implementation
        word_count = len(content.split())
        if word_count < 100:
            return "easy"
        elif word_count < 500:
            return "medium"
        else:
            return "hard"
    
    def _estimate_study_time(self, content: str, difficulty: str) -> int:
        """Estimate study time in minutes."""
        word_count = len(content.split())
        base_time = word_count // 50  # 50 words per minute reading
        
        if difficulty == "easy":
            return base_time
        elif difficulty == "medium":
            return base_time * 1.5
        else:
            return base_time * 2
    
    def _identify_prerequisites(self, content: str, subject: str) -> List[str]:
        """Identify prerequisites for the content."""
        # Simplified implementation
        return [f"Basic {subject} knowledge"]
    
    def _define_learning_objectives(self, content: str, subject: str) -> List[str]:
        """Define learning objectives for the content."""
        # Simplified implementation
        return [
            f"Understand key concepts in {subject}",
            f"Apply {subject} principles",
            f"Analyze {subject} problems"
        ]
    
    def _suggest_activities(
        self, 
        content: str, 
        subject: str, 
        difficulty: str
    ) -> List[str]:
        """Suggest learning activities."""
        activities = [
            "Review key concepts",
            "Practice with examples",
            "Create summary notes"
        ]
        
        if difficulty == "hard":
            activities.extend([
                "Break down complex topics",
                "Seek additional resources",
                "Practice with peers"
            ])
        
        return activities
    
    def _generate_analysis_summary(self, analysis: ContentAnalysis) -> str:
        """Generate a summary of content analysis."""
        summary = f"""
📊 Content Analysis Summary

🎯 Key Concepts: {', '.join(analysis.key_concepts[:5])}
📈 Difficulty Level: {analysis.difficulty_level.title()}
⏱️ Estimated Study Time: {analysis.estimated_study_time} minutes
📚 Prerequisites: {', '.join(analysis.prerequisites)}
🎓 Learning Objectives: {', '.join(analysis.learning_objectives[:3])}
🔧 Suggested Activities: {', '.join(analysis.suggested_activities[:3])}
        """
        return summary.strip()
    
    async def _handle_unknown_task(
        self, 
        task: Dict[str, Any], 
        context: Optional[Dict[str, Any]] = None
    ) -> AgentResponse:
        """Handle unknown task types."""
        task_type = task.get("type", "unknown")
        
        self.logger.warning(
            "Unknown task type received",
            task_type=task_type,
            task=task
        )
        
        return AgentResponse(
            content=f"Unknown task type: {task_type}",
            metadata={"task": task},
            success=False,
            error=f"Unsupported task type: {task_type}"
        )
    
    def get_capabilities(self) -> List[str]:
        """Get the capabilities of the Notewriter Agent."""
        return [
            "Academic content analysis and processing",
            "Personalized study material generation",
            "Learning style adaptation",
            "Note-taking and summarization",
            "Quiz and assessment creation",
            "Flashcard generation",
            "Visual aid creation",
            "Content optimization for different learners"
        ]
    
    def get_student_materials(self, student_id: str) -> List[StudyMaterial]:
        """Get all study materials for a specific student."""
        return self.material_database.get(student_id, [])
    
    def get_content_analysis(self, content_key: str) -> Optional[ContentAnalysis]:
        """Get content analysis by key."""
        return self.content_analyses.get(content_key)
