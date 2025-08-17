"""
Assessment Service for the Ascend system.

This service handles student assessment logic, including learning preference analysis,
cognitive style assessment, and academic commitment tracking.
"""

from typing import Any, Dict, List, Optional
from datetime import datetime

from config.logging_config import LoggerMixin


class AssessmentService(LoggerMixin):
    """
    Service for handling student assessments and evaluations.
    
    This service provides functionality for:
    - Learning preference analysis
    - Cognitive style assessment
    - Academic commitment tracking
    - Challenge identification
    - Assessment result processing
    """
    
    def __init__(self):
        """Initialize the Assessment Service."""
        self.assessments = {}
        self.assessment_templates = self._initialize_assessment_templates()
        
    def _initialize_assessment_templates(self) -> Dict[str, Any]:
        """Initialize assessment templates for different types of evaluations."""
        return {
            "learning_preferences": {
                "visual": {
                    "questions": [
                        "I prefer to learn through diagrams and charts",
                        "I remember information better when I see it written down",
                        "I like to use color coding in my notes"
                    ],
                    "weight": 1.0
                },
                "auditory": {
                    "questions": [
                        "I prefer to learn through listening and discussion",
                        "I remember information better when I hear it explained",
                        "I like to study with background music or sounds"
                    ],
                    "weight": 1.0
                },
                "kinesthetic": {
                    "questions": [
                        "I prefer to learn through hands-on activities",
                        "I remember information better when I physically do something",
                        "I like to move around while studying"
                    ],
                    "weight": 1.0
                },
                "reading": {
                    "questions": [
                        "I prefer to learn through reading and writing",
                        "I remember information better when I read it",
                        "I like to take detailed notes while studying"
                    ],
                    "weight": 1.0
                }
            },
            "cognitive_style": {
                "analytical": {
                    "indicators": ["logical thinking", "step-by-step approach", "detail-oriented"],
                    "weight": 1.0
                },
                "creative": {
                    "indicators": ["intuitive thinking", "holistic approach", "big-picture oriented"],
                    "weight": 1.0
                },
                "practical": {
                    "indicators": ["hands-on learning", "real-world application", "problem-solving"],
                    "weight": 1.0
                }
            }
        }
    
    async def conduct_learning_preference_assessment(
        self, 
        student_id: str, 
        responses: Dict[str, List[int]]
    ) -> Dict[str, Any]:
        """
        Conduct learning preference assessment.
        
        Args:
            student_id: Student identifier
            responses: Student responses to assessment questions
            
        Returns:
            Assessment results with preference scores
        """
        try:
            self.logger.info(f"Conducting learning preference assessment for student {student_id}")
            
            # Calculate preference scores
            preference_scores = self._calculate_preference_scores(responses)
            
            # Determine primary and secondary learning styles
            primary_style, secondary_style = self._determine_learning_styles(preference_scores)
            
            # Create assessment result
            assessment_result = {
                "student_id": student_id,
                "assessment_type": "learning_preferences",
                "preference_scores": preference_scores,
                "primary_learning_style": primary_style,
                "secondary_learning_style": secondary_style,
                "recommendations": self._generate_learning_recommendations(preference_scores),
                "conducted_at": datetime.now().isoformat()
            }
            
            # Store assessment result
            self.assessments[student_id] = assessment_result
            
            self.logger.info(f"Learning preference assessment completed for student {student_id}")
            
            return assessment_result
            
        except Exception as e:
            self.logger.error(f"Learning preference assessment failed for student {student_id}: {e}")
            raise
    
    async def conduct_cognitive_style_assessment(
        self, 
        student_id: str, 
        responses: Dict[str, List[int]]
    ) -> Dict[str, Any]:
        """
        Conduct cognitive style assessment.
        
        Args:
            student_id: Student identifier
            responses: Student responses to cognitive style questions
            
        Returns:
            Assessment results with cognitive style analysis
        """
        try:
            self.logger.info(f"Conducting cognitive style assessment for student {student_id}")
            
            # Calculate cognitive style scores
            style_scores = self._calculate_cognitive_style_scores(responses)
            
            # Determine dominant cognitive style
            dominant_style = self._determine_dominant_cognitive_style(style_scores)
            
            # Create assessment result
            assessment_result = {
                "student_id": student_id,
                "assessment_type": "cognitive_style",
                "style_scores": style_scores,
                "dominant_cognitive_style": dominant_style,
                "learning_implications": self._generate_cognitive_style_implications(style_scores),
                "conducted_at": datetime.now().isoformat()
            }
            
            # Update existing assessment or create new one
            if student_id in self.assessments:
                self.assessments[student_id].update(assessment_result)
            else:
                self.assessments[student_id] = assessment_result
            
            self.logger.info(f"Cognitive style assessment completed for student {student_id}")
            
            return assessment_result
            
        except Exception as e:
            self.logger.error(f"Cognitive style assessment failed for student {student_id}: {e}")
            raise
    
    async def track_academic_commitments(
        self, 
        student_id: str, 
        commitments: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Track academic commitments and workload.
        
        Args:
            student_id: Student identifier
            commitments: List of academic commitments
            
        Returns:
            Commitment analysis and recommendations
        """
        try:
            self.logger.info(f"Tracking academic commitments for student {student_id}")
            
            # Analyze workload
            workload_analysis = self._analyze_workload(commitments)
            
            # Identify potential challenges
            challenges = self._identify_potential_challenges(commitments, workload_analysis)
            
            # Generate recommendations
            recommendations = self._generate_commitment_recommendations(workload_analysis, challenges)
            
            # Create commitment tracking result
            tracking_result = {
                "student_id": student_id,
                "tracking_type": "academic_commitments",
                "commitments": commitments,
                "workload_analysis": workload_analysis,
                "identified_challenges": challenges,
                "recommendations": recommendations,
                "tracked_at": datetime.now().isoformat()
            }
            
            # Update existing assessment or create new one
            if student_id in self.assessments:
                self.assessments[student_id].update(tracking_result)
            else:
                self.assessments[student_id] = tracking_result
            
            self.logger.info(f"Academic commitment tracking completed for student {student_id}")
            
            return tracking_result
            
        except Exception as e:
            self.logger.error(f"Academic commitment tracking failed for student {student_id}: {e}")
            raise
    
    async def identify_support_needs(
        self, 
        student_id: str, 
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Identify specific support needs based on assessment data.
        
        Args:
            student_id: Student identifier
            context: Additional context for support identification
            
        Returns:
            Support needs analysis and recommendations
        """
        try:
            self.logger.info(f"Identifying support needs for student {student_id}")
            
            # Get existing assessment data
            assessment_data = self.assessments.get(student_id, {})
            
            # Analyze support needs
            support_needs = self._analyze_support_needs(assessment_data, context)
            
            # Prioritize support areas
            prioritized_needs = self._prioritize_support_needs(support_needs)
            
            # Generate support strategies
            support_strategies = self._generate_support_strategies(prioritized_needs)
            
            # Create support needs result
            support_result = {
                "student_id": student_id,
                "analysis_type": "support_needs",
                "support_needs": support_needs,
                "prioritized_needs": prioritized_needs,
                "support_strategies": support_strategies,
                "analysis_date": datetime.now().isoformat()
            }
            
            # Update existing assessment
            if student_id in self.assessments:
                self.assessments[student_id].update(support_result)
            else:
                self.assessments[student_id] = support_result
            
            self.logger.info(f"Support needs identification completed for student {student_id}")
            
            return support_result
            
        except Exception as e:
            self.logger.error(f"Support needs identification failed for student {student_id}: {e}")
            raise
    
    def _calculate_preference_scores(self, responses: Dict[str, List[int]]) -> Dict[str, float]:
        """Calculate preference scores from student responses."""
        scores = {}
        
        for style, responses_list in responses.items():
            if responses_list:
                # Calculate average response (assuming 1-5 scale)
                avg_response = sum(responses_list) / len(responses_list)
                scores[style] = avg_response / 5.0  # Normalize to 0-1 scale
        
        return scores
    
    def _determine_learning_styles(self, scores: Dict[str, float]) -> tuple:
        """Determine primary and secondary learning styles from scores."""
        sorted_styles = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        
        if len(sorted_styles) >= 2:
            return sorted_styles[0][0], sorted_styles[1][0]
        elif len(sorted_styles) == 1:
            return sorted_styles[0][0], None
        else:
            return "mixed", None
    
    def _generate_learning_recommendations(self, scores: Dict[str, float]) -> List[str]:
        """Generate learning recommendations based on preference scores."""
        recommendations = []
        
        for style, score in scores.items():
            if score > 0.7:  # Strong preference
                if style == "visual":
                    recommendations.append("Use diagrams, charts, and mind maps for studying")
                elif style == "auditory":
                    recommendations.append("Participate in study groups and discussions")
                elif style == "kinesthetic":
                    recommendations.append("Use hands-on activities and movement while studying")
                elif style == "reading":
                    recommendations.append("Take detailed notes and read extensively")
        
        return recommendations
    
    def _calculate_cognitive_style_scores(self, responses: Dict[str, List[int]]) -> Dict[str, float]:
        """Calculate cognitive style scores from responses."""
        scores = {}
        
        for style, responses_list in responses.items():
            if responses_list:
                avg_response = sum(responses_list) / len(responses_list)
                scores[style] = avg_response / 5.0
        
        return scores
    
    def _determine_dominant_cognitive_style(self, scores: Dict[str, float]) -> str:
        """Determine dominant cognitive style from scores."""
        if not scores:
            return "balanced"
        
        dominant_style = max(scores.items(), key=lambda x: x[1])
        return dominant_style[0]
    
    def _generate_cognitive_style_implications(self, scores: Dict[str, float]) -> List[str]:
        """Generate learning implications based on cognitive style."""
        implications = []
        
        for style, score in scores.items():
            if score > 0.6:
                if style == "analytical":
                    implications.append("Benefit from structured, logical approaches to learning")
                elif style == "creative":
                    implications.append("Thrive with open-ended, innovative learning methods")
                elif style == "practical":
                    implications.append("Learn best through real-world applications and examples")
        
        return implications
    
    def _analyze_workload(self, commitments: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze academic workload from commitments."""
        total_credits = sum(commitment.get("credits", 0) for commitment in commitments)
        total_hours = sum(commitment.get("estimated_hours", 0) for commitment in commitments)
        
        # Determine workload level
        if total_credits <= 12:
            workload_level = "light"
        elif total_credits <= 16:
            workload_level = "moderate"
        else:
            workload_level = "heavy"
        
        return {
            "total_credits": total_credits,
            "total_hours": total_hours,
            "workload_level": workload_level,
            "commitment_count": len(commitments)
        }
    
    def _identify_potential_challenges(self, commitments: List[Dict[str, Any]], workload: Dict[str, Any]) -> List[str]:
        """Identify potential challenges based on commitments and workload."""
        challenges = []
        
        if workload["workload_level"] == "heavy":
            challenges.append("High workload may lead to stress and time management issues")
        
        # Check for conflicting schedules
        schedules = [commitment.get("schedule", {}) for commitment in commitments]
        if self._has_schedule_conflicts(schedules):
            challenges.append("Potential schedule conflicts detected")
        
        # Check for difficult subjects
        difficult_subjects = [c for c in commitments if c.get("difficulty", "medium") == "high"]
        if len(difficult_subjects) > 2:
            challenges.append("Multiple challenging subjects may require additional support")
        
        return challenges
    
    def _generate_commitment_recommendations(self, workload: Dict[str, Any], challenges: List[str]) -> List[str]:
        """Generate recommendations based on workload and challenges."""
        recommendations = []
        
        if workload["workload_level"] == "heavy":
            recommendations.append("Consider reducing course load or seeking academic advising")
        
        if challenges:
            recommendations.append("Develop a comprehensive time management strategy")
            recommendations.append("Seek tutoring or study group support for challenging subjects")
        
        recommendations.append("Create a detailed study schedule with regular breaks")
        
        return recommendations
    
    def _has_schedule_conflicts(self, schedules: List[Dict[str, Any]]) -> bool:
        """Check for schedule conflicts."""
        # Simplified implementation - in reality, this would be more sophisticated
        return False
    
    def _analyze_support_needs(self, assessment_data: Dict[str, Any], context: Dict[str, Any]) -> List[str]:
        """Analyze support needs based on assessment data."""
        needs = []
        
        # Analyze learning preferences
        if "preference_scores" in assessment_data:
            scores = assessment_data["preference_scores"]
            if scores.get("visual", 0) < 0.3:
                needs.append("Visual learning support")
            if scores.get("auditory", 0) < 0.3:
                needs.append("Auditory learning support")
        
        # Analyze workload
        if "workload_analysis" in assessment_data:
            workload = assessment_data["workload_analysis"]
            if workload.get("workload_level") == "heavy":
                needs.append("Time management support")
                needs.append("Stress management support")
        
        # Analyze challenges
        if "identified_challenges" in assessment_data:
            challenges = assessment_data["identified_challenges"]
            if "schedule conflicts" in str(challenges).lower():
                needs.append("Schedule coordination support")
        
        return needs
    
    def _prioritize_support_needs(self, needs: List[str]) -> List[Dict[str, Any]]:
        """Prioritize support needs based on urgency and impact."""
        priority_mapping = {
            "Time management support": 1,
            "Stress management support": 1,
            "Schedule coordination support": 2,
            "Visual learning support": 3,
            "Auditory learning support": 3
        }
        
        prioritized = []
        for need in needs:
            priority = priority_mapping.get(need, 4)
            prioritized.append({
                "need": need,
                "priority": priority,
                "urgency": "high" if priority <= 2 else "medium"
            })
        
        # Sort by priority
        prioritized.sort(key=lambda x: x["priority"])
        return prioritized
    
    def _generate_support_strategies(self, prioritized_needs: List[Dict[str, Any]]) -> Dict[str, List[str]]:
        """Generate support strategies for prioritized needs."""
        strategies = {}
        
        for need_info in prioritized_needs:
            need = need_info["need"]
            if "time management" in need.lower():
                strategies[need] = [
                    "Create detailed study schedule",
                    "Use time blocking techniques",
                    "Set realistic goals and deadlines"
                ]
            elif "stress management" in need.lower():
                strategies[need] = [
                    "Practice mindfulness and relaxation techniques",
                    "Maintain regular exercise routine",
                    "Seek counseling or support groups"
                ]
            elif "visual learning" in need.lower():
                strategies[need] = [
                    "Use mind maps and diagrams",
                    "Create visual study aids",
                    "Watch educational videos"
                ]
            elif "auditory learning" in need.lower():
                strategies[need] = [
                    "Participate in study groups",
                    "Record and listen to lectures",
                    "Use verbal repetition techniques"
                ]
            else:
                strategies[need] = ["Seek academic advising", "Connect with peer mentors"]
        
        return strategies
    
    def get_assessment(self, student_id: str) -> Optional[Dict[str, Any]]:
        """Get assessment data for a student."""
        return self.assessments.get(student_id)
    
    def get_all_assessments(self) -> Dict[str, Dict[str, Any]]:
        """Get all assessment data."""
        return self.assessments.copy()
    
    def update_assessment(self, student_id: str, updates: Dict[str, Any]):
        """Update assessment data for a student."""
        if student_id in self.assessments:
            self.assessments[student_id].update(updates)
        else:
            self.assessments[student_id] = updates
    
    def delete_assessment(self, student_id: str):
        """Delete assessment data for a student."""
        if student_id in self.assessments:
            del self.assessments[student_id]
