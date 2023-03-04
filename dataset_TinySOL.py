import pandas as pd
import scipy.io.wavfile as wavfile
from dataset_creation import chunks, extract_peaks_and_freqs, final_data_collection
from get_audio_from_link import obtain_youtube_link, delete_spaces, download_audio, remove_audio

common_path = '/home/jacs/Documents/DataScience/Personal/'
input_path = 'song_similarity_audio/TinySOL/'
output_path = 'song_similarity_audio/'

df_into = pd.read_csv(common_path+input_path+'TinySOL_metadata.csv')
df_into= df_into[df_into['Needed digital retuning']]
instruments = df_into['Instrument (in full)'].unique()

instruments

instruments_test = ['Trombone', 'Trumpet in C']
outputs = ['trombone/database_trombone_10_peaks', 'trumpet/database_trumpet_10_peaks']
#audio_files = ['A-sharp-trumpet', 'B-trumpet', 'C-sharp-trumpet', 'D-sharp-trumpet', 'E-trumpet', 'F-sharp-trumpet', 'G-sharp-trumpet']

#for linko in links:
#    title = download_audio(linko)
#    remove_audio(title)

for kk in range(0,len(instruments_test)):
    print(kk)
    instrument_dataset = instruments_test[kk]
    df_final = pd.DataFrame({'peak_1': [], 'peak_2': [], 'Magnitude difference': [],'instrument': [], 'note_played': []})
    for woko in df_into[df_into['Instrument (in full)'] == instrument_dataset]['Path']:
        wavo = common_path + woko
        titulo = woko.split('/')[-1]
        #    file_1 = file.format(audio_1)
        #    wavo = path + file_1
        Fs, audio = wavfile.read(wavo)
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
            df_final_2 = final_data_collection(freq_sorted, pikos_sorted, 10, kk, titulo).reset_index(drop=True)
            df_final = df_final.append(df_final_2).reset_index(drop=True)
    df_final=df_final.reset_index(drop=True)
    df_final.to_csv(common_path+output_path+outputs[kk]+'.csv', index=False)
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