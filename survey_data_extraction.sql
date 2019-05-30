USE [CherwellPROD]
SELECT
	 SE.Technician,
	 SE.TechnicianTeam,
	 SE.SurveyTaker,
	 SE.Score,
	 I.Service,
	 I.Category,
	 I.Subcategory,
	 I.Priority,
	 I.Source,
	 I.CreatedDateTime,
	 I.Stat_DateTimeResolved,
	 I.Stat_SLAResponseBreached,
	 I.Stat_SLAResolutionBreached
FROM
	SurveyElement AS SE --Survey table
	JOIN Incident AS I ON SE.ParentRecID = I.RecID --Incident table
WHERE
	SE.SurveyElementTypeName = 'Survey'
	AND NOT SE.CompletedDateTime = '' --Exclude incomplete survyes
	AND NOT SE.Score = 0 --Survey with 0 score are considered incomplete (it is not possible to score 0)
