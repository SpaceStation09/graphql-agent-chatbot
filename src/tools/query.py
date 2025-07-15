IDENTITY_QUERY = '''
query QUERY_PROFILE($platform: Platform!, $identity: String!) {
	identity(platform: $platform, identity: $identity) {
		id
		status
		aliases
		identity
		platform
		network
		isPrimary
		primaryName
		resolvedAddress {
			address
			network
		}
		ownerAddress {
			address
			network
		}
		managerAddress {
			address
			network
		}
		updatedAt
		profile {
			identity
			platform
			network
			address
			displayName
			avatar
			description
			addresses {
				address
				network
			}
		}
		identityGraph {
			graphId
			vertices {
				identity
				platform
				network
				isPrimary
				primaryName
				registeredAt
				managerAddress {
					address
					network
				}
				ownerAddress {
					address
					network
				}
				resolvedAddress {
					address
					network
				}
				updatedAt
				expiredAt
				profile {
					uid
					identity
					platform
					network
					address
					displayName
					avatar
					description
					texts
					addresses {
						address
						network
					}
				}
			}
		}
	}
}
'''

INTROSPECTION_QUERY = '''
query {
  __schema {
    queryType {
      name
    }
    types {
      name
      kind
      fields {
        name
        description
        type {
          name
          kind
          ofType {
            name
            kind
          }
        }
      }
    }
  }
}
'''