import requests

url = "https://apis.justwatch.com/graphql"
query = {
    "operationName": "GetPopularTitles",
    "variables": {
        "popularTitlesSortBy": "POPULAR",
        "first": 40,
        "platform": "WEB",
        "sortRandomSeed": 0,
        "popularAfterCursor": "NDA=",
        "popularTitlesFilter": {
            "ageCertifications": [],
            "excludeGenres": [],
            "excludeProductionCountries": [],
            "genres": [],
            "objectTypes": [],
            "productionCountries": [],
            "packages": ["amp", "dnp", "hay"],
            "excludeIrrelevantTitles": False,
            "presentationTypes": [],
            "monetizationTypes": [],
        },
        "watchNowFilter": {"packages": ["amp", "dnp", "hay"], "monetizationTypes": []},
        "language": "en",
        "country": "GB",
    },
    "query": """
query GetPopularTitles($country: Country!, $popularTitlesFilter: TitleFilter, $watchNowFilter: WatchNowOfferFilter!, $popularAfterCursor: String, $popularTitlesSortBy: PopularTitlesSorting! = POPULAR, $first: Int! = 40, $language: Language!, $platform: Platform! = WEB, $sortRandomSeed: Int! = 0, $profile: PosterProfile, $backdropProfile: BackdropProfile, $format: ImageFormat) {
  popularTitles(
    country: $country
    filter: $popularTitlesFilter
    after: $popularAfterCursor
    sortBy: $popularTitlesSortBy
    first: $first
    sortRandomSeed: $sortRandomSeed
  ) {
    totalCount
    pageInfo {
      startCursor
      endCursor
      hasPreviousPage
      hasNextPage
      __typename
    }
    edges {
      ...PopularTitleGraphql
      __typename
    }
    __typename
  }
}

fragment PopularTitleGraphql on PopularTitlesEdge {
  cursor
  node {
    id
    objectId
    objectType
    content(country: $country, language: $language) {
      title
      fullPath
      scoring {
        imdbScore
        __typename
      }
      posterUrl(profile: $profile, format: $format)
      ... on ShowContent {
        backdrops(profile: $backdropProfile, format: $format) {
          backdropUrl
          __typename
        }
        __typename
      }
      __typename
    }
    likelistEntry {
      createdAt
      __typename
    }
    dislikelistEntry {
      createdAt
      __typename
    }
    watchlistEntry {
      createdAt
      __typename
    }
    watchNowOffer(country: $country, platform: $platform, filter: $watchNowFilter) {
      id
      standardWebURL
      package {
        packageId
        clearName
        __typename
      }
      retailPrice(language: $language)
      retailPriceValue
      lastChangeRetailPriceValue
      currency
      presentationType
      monetizationType
      availableTo
      __typename
    }
    ... on Movie {
      seenlistEntry {
        createdAt
        __typename
      }
      __typename
    }
    ... on Show {
      seenState(country: $country) {
        seenEpisodeCount
        progress
        __typename
      }
      __typename
    }
    __typename
  }
  __typename
}
""",
}

response = requests.post(url, json=query)
print(response.json())