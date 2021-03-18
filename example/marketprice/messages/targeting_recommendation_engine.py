"""Schema definitions for `marketprice.messages.targeting_recommendation_engine` namespace. Generated by avro2py v.0.0.4."""
import datetime
import decimal
import enum
from typing import List, NamedTuple, Union


class TargetingRecommendationToEnricher(NamedTuple):
    """
    Provides required information to the TRE serving layer:
    mprice/v0/targeting-recommendation-to-enricher
    """

    product: "TargetingRecommendationProduct"
    entityType: "TargetingRecommendationToEnricher.EntityType"
    targetingClause: str
    sentAt: datetime.datetime
    _original_schema = (
        '{"type": "record", "name": "TargetingRecommendationToEnricher", "namespace":'
        ' "marketprice.messages.targeting_recommendation_engine", "doc": "Provides'
        " required information to the TRE serving layer:"
        ' mprice/v0/targeting-recommendation-to-enricher", "fields": [{"name":'
        ' "product", "type": {"type": "record", "name":'
        ' "TargetingRecommendationProduct", "doc": "product that requires a targeting'
        ' recommendation: mprice/v0/targeting-recommendation-product", "fields":'
        ' [{"name": "productIdentifier", "type": [{"type": "record", "name":'
        ' "Nile1pProduct", "namespace":'
        ' "marketprice.messages.targeting_recommendation_engine.TargetingRecommendationProduct.ProductIdentifier",'
        ' "fields": [{"name": "vendorId", "type": "string"}, {"name": "marketplaceId",'
        ' "type": "string"}, {"name": "nsin", "type": "string"}]}, {"type": "record",'
        ' "name": "NileProduct", "namespace":'
        ' "marketprice.messages.targeting_recommendation_engine.TargetingRecommendationProduct.ProductIdentifier",'
        ' "fields": [{"name": "sellerId", "type": "string"}, {"name": "marketplaceId",'
        ' "type": "string"}, {"name": "sku", "type": "string"}]}, {"type": "record",'
        ' "name": "WallyworldProduct", "namespace":'
        ' "marketprice.messages.targeting_recommendation_engine.TargetingRecommendationProduct.ProductIdentifier",'
        ' "fields": [{"name": "advertiserId", "type": "long"}, {"name": "itemId",'
        ' "type": "string"}]}]}, {"name": "sentAt", "type": {"type": "long",'
        ' "logicalType": "timestamp-millis"}}]}}, {"name": "entityType", "type":'
        ' {"type": "enum", "name": "EntityType", "namespace":'
        ' "marketprice.messages.targeting_recommendation_engine.TargetingRecommendationToEnricher",'
        ' "doc": "The entity type for the targeting clause: ", "symbols": ["SPTarget",'
        ' "SPKeyword", "SBKeyword", "AdGroup", "WallyworldKeyword",'
        ' "WallyworldAdItem"]}}, {"name": "targetingClause", "type": "string"},'
        ' {"name": "sentAt", "type": {"type": "long", "logicalType":'
        ' "timestamp-millis"}}]}'
    )

    @enum.unique
    class EntityType(enum.Enum):
        """
        The entity type for the targeting clause:
        """

        AD_GROUP = "AdGroup"
        SBKEYWORD = "SBKeyword"
        SPKEYWORD = "SPKeyword"
        SPTARGET = "SPTarget"
        WALLYWORLD_AD_ITEM = "WallyworldAdItem"
        WALLYWORLD_KEYWORD = "WallyworldKeyword"


class TargetingRecommendationProduct(NamedTuple):
    """
    product that requires a targeting recommendation:
    mprice/v0/targeting-recommendation-product
    """

    productIdentifier: Union[
        "TargetingRecommendationProduct.ProductIdentifier.Nile1pProduct",
        "TargetingRecommendationProduct.ProductIdentifier.NileProduct",
        "TargetingRecommendationProduct.ProductIdentifier.WallyworldProduct",
    ]
    sentAt: datetime.datetime
    _original_schema = (
        '{"type": "record", "name": "TargetingRecommendationProduct", "doc": "product'
        " that requires a targeting recommendation:"
        ' mprice/v0/targeting-recommendation-product", "fields": [{"name":'
        ' "productIdentifier", "type": [{"type": "record", "name": "Nile1pProduct",'
        ' "namespace":'
        ' "marketprice.messages.targeting_recommendation_engine.TargetingRecommendationProduct.ProductIdentifier",'
        ' "fields": [{"name": "vendorId", "type": "string"}, {"name": "marketplaceId",'
        ' "type": "string"}, {"name": "nsin", "type": "string"}]}, {"type": "record",'
        ' "name": "NileProduct", "namespace":'
        ' "marketprice.messages.targeting_recommendation_engine.TargetingRecommendationProduct.ProductIdentifier",'
        ' "fields": [{"name": "sellerId", "type": "string"}, {"name": "marketplaceId",'
        ' "type": "string"}, {"name": "sku", "type": "string"}]}, {"type": "record",'
        ' "name": "WallyworldProduct", "namespace":'
        ' "marketprice.messages.targeting_recommendation_engine.TargetingRecommendationProduct.ProductIdentifier",'
        ' "fields": [{"name": "advertiserId", "type": "long"}, {"name": "itemId",'
        ' "type": "string"}]}]}, {"name": "sentAt", "type": {"type": "long",'
        ' "logicalType": "timestamp-millis"}}]}'
    )

    class ProductIdentifier:
        class WallyworldProduct(NamedTuple):
            advertiserId: int
            itemId: str
            _original_schema = (
                '{"type": "record", "name": "WallyworldProduct", "namespace":'
                ' "marketprice.messages.targeting_recommendation_engine.TargetingRecommendationProduct.ProductIdentifier",'
                ' "fields": [{"name": "advertiserId", "type": "long"}, {"name":'
                ' "itemId", "type": "string"}]}'
            )

        class NileProduct(NamedTuple):
            sellerId: str
            marketplaceId: str
            sku: str
            _original_schema = (
                '{"type": "record", "name": "NileProduct", "namespace":'
                ' "marketprice.messages.targeting_recommendation_engine.TargetingRecommendationProduct.ProductIdentifier",'
                ' "fields": [{"name": "sellerId", "type": "string"}, {"name":'
                ' "marketplaceId", "type": "string"}, {"name": "sku", "type":'
                ' "string"}]}'
            )

        class Nile1pProduct(NamedTuple):
            vendorId: str
            marketplaceId: str
            nsin: str
            _original_schema = (
                '{"type": "record", "name": "Nile1pProduct", "namespace":'
                ' "marketprice.messages.targeting_recommendation_engine.TargetingRecommendationProduct.ProductIdentifier",'
                ' "fields": [{"name": "vendorId", "type": "string"}, {"name":'
                ' "marketplaceId", "type": "string"}, {"name": "nsin", "type":'
                ' "string"}]}'
            )


class TargetingRecommendation(NamedTuple):
    """
    targeting recommendation engine decisions: mprice/v0/targeting-recommendation
    """

    profileId: int
    campaignId: int
    adGroupId: int
    sku: str
    bid: decimal.Decimal
    recommendationScore: decimal.Decimal
    recommendedAt: datetime.datetime
    Recommendation: Union[
        "TargetingRecommendation.Keyword",
        "TargetingRecommendation.ProductAttributeTarget",
    ]
    _original_schema = (
        '{"type": "record", "name": "TargetingRecommendation", "namespace":'
        ' "marketprice.messages.targeting_recommendation_engine", "doc": "targeting'
        ' recommendation engine decisions: mprice/v0/targeting-recommendation",'
        ' "fields": [{"name": "profileId", "type": "long"}, {"name": "campaignId",'
        ' "type": "long"}, {"name": "adGroupId", "type": "long"}, {"name": "sku",'
        ' "type": "string"}, {"name": "bid", "type": {"type": "bytes", "logicalType":'
        ' "decimal", "precision": 21, "scale": 2}}, {"name": "recommendationScore",'
        ' "type": {"type": "bytes", "logicalType": "decimal", "precision": 21, "scale":'
        ' 2}}, {"name": "recommendedAt", "type": {"type": "long", "logicalType":'
        ' "timestamp-millis"}}, {"name": "Recommendation", "type": [{"type": "record",'
        ' "name": "Keyword", "namespace":'
        ' "marketprice.messages.targeting_recommendation_engine.TargetingRecommendation",'
        ' "doc": "keyword description", "fields": [{"name": "keywordText", "type":'
        ' "string"}, {"name": "matchType", "type": {"type": "enum", "name":'
        ' "KeywordMatchType", "symbols": ["exact", "phrase", "broad"]}}, {"name":'
        ' "keywordState", "type": {"type": "enum", "name": "KeywordState", "doc":'
        ' "Possible states of a keyword", "symbols": ["enabled", "paused",'
        ' "archived"]}}]}, {"type": "record", "name": "ProductAttributeTarget",'
        ' "namespace":'
        ' "marketprice.messages.targeting_recommendation_engine.TargetingRecommendation",'
        ' "doc": "PAT expression description", "fields": [{"name": "expression",'
        ' "type": {"type": "array", "items": {"type": "record", "name": "Predicate",'
        ' "doc": "Predicate of PAT expression for target recommendation", "fields":'
        ' [{"name": "predicateType", "type": {"type": "enum", "name": "PredicateType",'
        ' "doc": "Types of PAT expression predicate enum", "symbols":'
        ' ["queryBroadMatches", "queryPhraseMatches", "queryExactMatches",'
        ' "nsinCategorySameAs", "nsinBrandSameAs", "nsinPriceLessThan",'
        ' "nsinPriceBetween", "nsinPriceGreaterThan", "nsinReviewRatingLessThan",'
        ' "nsinReviewRatingBetween", "nsinReviewRatingGreaterThan", "nsinSameAs",'
        ' "queryBroadRelMatches", "queryHighRelMatches", "nsinSubstituteRelated",'
        ' "nsinAccessoryRelated", "nsinAgeRangeSameAs", "nsinGenreSameAs",'
        ' "nsinIsPrimeShippingEligible"]}}, {"name": "value", "type": "string"}]}}},'
        ' {"name": "expressionType", "type": {"type": "enum", "name": "ExpressionType",'
        ' "doc": "Possible types of an expression", "symbols": ["auto", "manual"]}},'
        ' {"name": "expressionState", "type": "KeywordState"}]}]}]}'
    )

    class ProductAttributeTarget(NamedTuple):
        """
        PAT expression description
        """

        expression: List["TargetingRecommendation.Predicate"]
        expressionType: "TargetingRecommendation.ExpressionType"
        expressionState: "TargetingRecommendation.KeywordState"
        _original_schema = (
            '{"type": "record", "name": "ProductAttributeTarget", "namespace":'
            ' "marketprice.messages.targeting_recommendation_engine.TargetingRecommendation",'
            ' "doc": "PAT expression description", "fields": [{"name": "expression",'
            ' "type": {"type": "array", "items": {"type": "record", "name":'
            ' "Predicate", "doc": "Predicate of PAT expression for target'
            ' recommendation", "fields": [{"name": "predicateType", "type": {"type":'
            ' "enum", "name": "PredicateType", "doc": "Types of PAT expression'
            ' predicate enum", "symbols": ["queryBroadMatches", "queryPhraseMatches",'
            ' "queryExactMatches", "nsinCategorySameAs", "nsinBrandSameAs",'
            ' "nsinPriceLessThan", "nsinPriceBetween", "nsinPriceGreaterThan",'
            ' "nsinReviewRatingLessThan", "nsinReviewRatingBetween",'
            ' "nsinReviewRatingGreaterThan", "nsinSameAs", "queryBroadRelMatches",'
            ' "queryHighRelMatches", "nsinSubstituteRelated", "nsinAccessoryRelated",'
            ' "nsinAgeRangeSameAs", "nsinGenreSameAs",'
            ' "nsinIsPrimeShippingEligible"]}}, {"name": "value", "type":'
            ' "string"}]}}}, {"name": "expressionType", "type": {"type": "enum",'
            ' "name": "ExpressionType", "doc": "Possible types of an expression",'
            ' "symbols": ["auto", "manual"]}}, {"name": "expressionState", "type":'
            ' "KeywordState"}]}'
        )

    @enum.unique
    class ExpressionType(enum.Enum):
        """
        Possible types of an expression
        """

        AUTO = "auto"
        MANUAL = "manual"

    class Predicate(NamedTuple):
        """
        Predicate of PAT expression for target recommendation
        """

        predicateType: "TargetingRecommendation.PredicateType"
        value: str
        _original_schema = (
            '{"type": "record", "name": "Predicate", "doc": "Predicate of PAT'
            ' expression for target recommendation", "fields": [{"name":'
            ' "predicateType", "type": {"type": "enum", "name": "PredicateType", "doc":'
            ' "Types of PAT expression predicate enum", "symbols":'
            ' ["queryBroadMatches", "queryPhraseMatches", "queryExactMatches",'
            ' "nsinCategorySameAs", "nsinBrandSameAs", "nsinPriceLessThan",'
            ' "nsinPriceBetween", "nsinPriceGreaterThan", "nsinReviewRatingLessThan",'
            ' "nsinReviewRatingBetween", "nsinReviewRatingGreaterThan", "nsinSameAs",'
            ' "queryBroadRelMatches", "queryHighRelMatches", "nsinSubstituteRelated",'
            ' "nsinAccessoryRelated", "nsinAgeRangeSameAs", "nsinGenreSameAs",'
            ' "nsinIsPrimeShippingEligible"]}}, {"name": "value", "type": "string"}]}'
        )

    @enum.unique
    class PredicateType(enum.Enum):
        """
        Types of PAT expression predicate enum
        """

        NSIN_ACCESSORY_RELATED = "nsinAccessoryRelated"
        NSIN_AGE_RANGE_SAME_AS = "nsinAgeRangeSameAs"
        NSIN_BRAND_SAME_AS = "nsinBrandSameAs"
        NSIN_CATEGORY_SAME_AS = "nsinCategorySameAs"
        NSIN_GENRE_SAME_AS = "nsinGenreSameAs"
        NSIN_IS_PRIME_SHIPPING_ELIGIBLE = "nsinIsPrimeShippingEligible"
        NSIN_PRICE_BETWEEN = "nsinPriceBetween"
        NSIN_PRICE_GREATER_THAN = "nsinPriceGreaterThan"
        NSIN_PRICE_LESS_THAN = "nsinPriceLessThan"
        NSIN_REVIEW_RATING_BETWEEN = "nsinReviewRatingBetween"
        NSIN_REVIEW_RATING_GREATER_THAN = "nsinReviewRatingGreaterThan"
        NSIN_REVIEW_RATING_LESS_THAN = "nsinReviewRatingLessThan"
        NSIN_SAME_AS = "nsinSameAs"
        NSIN_SUBSTITUTE_RELATED = "nsinSubstituteRelated"
        QUERY_BROAD_MATCHES = "queryBroadMatches"
        QUERY_BROAD_REL_MATCHES = "queryBroadRelMatches"
        QUERY_EXACT_MATCHES = "queryExactMatches"
        QUERY_HIGH_REL_MATCHES = "queryHighRelMatches"
        QUERY_PHRASE_MATCHES = "queryPhraseMatches"

    class Keyword(NamedTuple):
        """
        keyword description
        """

        keywordText: str
        matchType: "TargetingRecommendation.KeywordMatchType"
        keywordState: "TargetingRecommendation.KeywordState"
        _original_schema = (
            '{"type": "record", "name": "Keyword", "namespace":'
            ' "marketprice.messages.targeting_recommendation_engine.TargetingRecommendation",'
            ' "doc": "keyword description", "fields": [{"name": "keywordText", "type":'
            ' "string"}, {"name": "matchType", "type": {"type": "enum", "name":'
            ' "KeywordMatchType", "symbols": ["exact", "phrase", "broad"]}}, {"name":'
            ' "keywordState", "type": {"type": "enum", "name": "KeywordState", "doc":'
            ' "Possible states of a keyword", "symbols": ["enabled", "paused",'
            ' "archived"]}}]}'
        )

    @enum.unique
    class KeywordState(enum.Enum):
        """
        Possible states of a keyword
        """

        ARCHIVED = "archived"
        ENABLED = "enabled"
        PAUSED = "paused"

    @enum.unique
    class KeywordMatchType(enum.Enum):
        BROAD = "broad"
        EXACT = "exact"
        PHRASE = "phrase"
