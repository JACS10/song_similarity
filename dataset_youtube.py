import pandas as pd
import scipy.io.wavfile as wavfile
from dataset_creation import chunks, extract_peaks_and_freqs, final_data_collection
from get_audio_from_link import obtain_youtube_link, delete_spaces, download_audio, remove_audio, from_mp4_to_wav

common_path = '/home/jacs/Documents/DataScience/Personal/'

dummy_path = 'song_similarity/'
# As an input there is going to be a list of youtube links that contain audio that can be
# usefull to expand and enrich the database of that particular instrument

# As an input we want a tupple, with the link as first position and instrument as second position

input_path = 'song_similarity_audio/trumpet/'

df_links = pd.read_csv(common_path+input_path+'trumpet_youtube_database_enrichment.csv')

print(df_links)

links_audio = list(df_links['youtube_links'])
titles = list(df_links['title'])

for kk in range(0,len(links_audio)):
    linko = links_audio[kk]
    title_file = str(download_audio(linko))
    database_name = str(titles[kk])
    df_final = pd.DataFrame({'peak_1': [], 'peak_2': [], 'Magnitude difference': [],'instrument': [], 'note_played': []})
    print(title_file)
    print(database_name)
    try:
        Fs, audio = wavfile.read(title_file+'.wav')
    except:
        from_mp4_to_wav(title_file+'.mp4',common_path+dummy_path)
        Fs, audio = wavfile.read(title_file+'.wav')
        remove_audio(title_file+'.mp4')
    length = audio.shape[0] / Fs
    audio_chunks = chunks(audio,int(length)*2)
    print(f"length = {length}s")
    for aud in audio_chunks[2:-2]:
        length_2 = aud.shape[0] / Fs
        #        print(Fs)
        # select left channel only
        try:
            aud = aud[:,0]
            print('plop')
        except:
            aud = aud[:]
        print('anti-plop')
        pikos_sorted, freq_sorted, sp_final, peaks  = extract_peaks_and_freqs(aud, Fs)
        df_final_2 = final_data_collection(freq_sorted, pikos_sorted, 10, kk, title_file).reset_index(drop=True)
        df_final = df_final.append(df_final_2).reset_index(drop=True)
    df_final=df_final.reset_index(drop=True)
    df_final.to_csv(common_path+input_path+database_name+'.csv', index=False)
remove_audio(title_file+'.wav')
    
#################################
#        plt.specgram(aud, Fs=Fs)
#        plt.xticks(time_cnk)    
#        plt.ylim(0,5000)
#        plt.title(titulo)
#        plt.show()
#        time = np.linspace(0., length_2, aud.shape[0])
#        plt.plot(time, aud)
#        plt.title('Original signal')
#        plt.show()
#        plt.plot(peaks, [sp_final[i] for i in peaks])
#        plt.plot(freq_sorted[:10], pikos_sorted[:10],'x')
#        plt.title('Final frequencies and intensities')
#        plt.show()
#        ss = np.fft.ifft(sp_final)
#        time = np.linspace(0., length_2, len(sp_final))
#        plt.plot(time, ss)
#        plt.title('Reconstruccion with data manipulation')
#        plt.show()
#################################