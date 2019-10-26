package main

import (
	"./paths"
	"github.com/fabioberger/airtable-go"
)

type airtableMediaLocation struct {
	AirtableID string              `json:"id,omitempty"`
	Fields     paths.MediaLocation `json:"fields"`
}

func OpenConnection(apiKey, baseID string) (*airtable.Client, error) {
	client, err := airtable.New(apiKey, baseID)
	if err != nil {
		return nil, err
	}
	return client, nil
}

func GetMediaLocations(tableName string, client *airtable.Client) []paths.MediaLocation {
	var records []airtableMediaLocation
	if err := client.ListRecords(tableName, &records); err != nil {
		return []paths.MediaLocation{}
	}
	var locs []paths.MediaLocation
	for i := range records {
		if len(records[i].Fields.Name) > 0 {
			locs = append(locs, records[i].Fields)
		}
	}
	return locs
}

func CreateMediaLocation(location paths.MediaLocation, tableName string, client *airtable.Client) (string, error) {
	record := airtableMediaLocation{Fields: location}
	var existingRecords []airtableMediaLocation
	if err := client.ListRecords(tableName, &existingRecords); err != nil {
		return "", err
	}
	for _, record := range existingRecords {
		if record.Fields.Name == location.Name {
			return UpdateMediaLocation(location, record.AirtableID, tableName, client)
		}
	}
	err := client.CreateRecord(tableName, &record)
	return record.AirtableID, err
}

func UpdateMediaLocation(location paths.MediaLocation, id, tableName string, client *airtable.Client) (string, error) {
	record := airtableMediaLocation{}
	err := client.UpdateRecord(tableName, id, map[string]interface{}{
		"Media Type":         location.MediaType,
		"Source Path":        location.RootPath,
		"Size":               location.Size,
		"Number of Episodes": location.NumberEpisodes,
		"Number of Seasons":  location.NumberSeasons,
	}, &record)
	return id, err
}

func MirrorMediaLocations(locations []paths.MediaLocation, tableName string, client *airtable.Client) (writes, updates, deletes uint, err error) {
	var existingRecords []airtableMediaLocation
	var existingIndex map[string]string
	existingIndex = make(map[string]string)
	if err := client.ListRecords(tableName, &existingRecords); err != nil {
		return
	}
	for _, record := range existingRecords {
		existingIndex[record.Fields.Name] = record.AirtableID
	}
	for _, loc := range locations {
		id, ok := existingIndex[loc.Name]
		if !ok {
			record := airtableMediaLocation{Fields: loc}
			_ = client.CreateRecord(tableName, &record)
			writes++
		} else {
			_, _ = UpdateMediaLocation(loc, id, tableName, client)
			updates++
		}
		existingIndex[loc.Name] = ""
	}
	for _, id := range existingIndex {
		if id != "" {
			_ = DeleteMediaLocation(id, tableName, client)
			deletes++
		}
	}
	return
}

func DeleteMediaLocation(id, tableName string, client *airtable.Client) error {
	return client.DestroyRecord(tableName, id)
}
